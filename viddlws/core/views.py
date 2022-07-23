#
#   VIDDLWS
#   Django project which uses youtube-dl to download and serve videos.
#   Copyright (C) 2017 Walter Reiner <walter.reiner@wreiner.at>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

# https://docs.djangoproject.com/en/1.10/topics/class-based-views/generic-display/

import logging

from braces.views import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from sesame.utils import get_token
from taggit.models import Tag

from viddlws.core.forms import VideoEditForm
from viddlws.core.models import Video, VideoStatus

# Get an instance of the logger
logger = logging.getLogger(__name__)


class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = "tags.html"

    context_object_name = "tags"
    login_url = "/login/"

    def get_queryset(self):
        queryset = (
            Tag.objects.filter(video__user=self.request.user)
            .exclude(name__in=["xxx", "private"])
            .distinct()
            .order_by("name")
        )
        return queryset


class VideoListView(LoginRequiredMixin, ListView):
    model = Video
    paginate_by = 9
    template_name = "index.html"

    context_object_name = "videos"
    login_url = "/accounts/login/"

    def get_queryset(self):
        try:
            tagslug = self.kwargs["slug"]
        except Exception:
            queryset = (
                Video.objects.filter(user=self.request.user)
                .exclude(tags__name__in=["xxx", "private"])
                .order_by("title")
            )
        else:
            queryset = Video.objects.filter(
                user=self.request.user, tags__slug=tagslug
            ).order_by("title")

        return queryset

    # https://stackoverflow.com/a/28533796
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        if "slug" in self.kwargs:
            context["tagslug"] = self.kwargs["slug"]
        return context


class VideoDetail(LoginRequiredMixin, DetailView):
    model = Video
    template_name = "video_detail.html"
    context_object_name = "video"
    login_url = "/accounts/login/"

    # def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
    # context = super(VideoDetail, self).get_context_data(**kwargs)
    # Add in a QuerySet of all the books
    # context['book_list'] = Book.objects.all()
    # return context


class VideoCreate(LoginRequiredMixin, CreateView):
    model = Video
    # http://stackoverflow.com/q/39020226/7523861
    form_class = VideoEditForm
    template_name = "video_form.html"

    success_url = "/"
    login_url = "/accounts/login/"

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get days to today for which no ratings exist
        # http://stackoverflow.com/a/31070622/7523861

        context["title"] = "VIDDLWS | Add Video"
        context["nav_section"] = "video"
        context["nav_sub_section"] = "add"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = VideoStatus.objects.get(status="new")
        return super().form_valid(form)


class VideoUpdate(LoginRequiredMixin, UpdateView):
    model = Video
    # http://stackoverflow.com/q/39020226/7523861
    form_class = VideoEditForm
    template_name = "video_form.html"

    success_url = "/"
    login_url = "/accounts/login/"

    def get_queryset(self):
        base_qs = super().get_queryset()
        return base_qs.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super().post(request, *args, **kwargs)


class VideoDelete(LoginRequiredMixin, DeleteView):
    model = Video
    template_name = "video_confirm_delete.html"

    success_url = "/"
    login_url = "/accounts/login/"

    def get_object(self, queryset=None):
        """Hook to ensure object is owned by request.user."""
        obj = super().get_object()
        if not obj.user == self.request.user:
            logger.warn("user tried to delete video entry which he does not own")
            raise Http404
        return obj

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super().post(request, *args, **kwargs)


@login_required
def create_sesame_token(request, slug):
    sesame_token = f"?sesame={get_token(request.user)}"
    context = {
        "tagslug": slug,
        "sesame_token": sesame_token,
    }
    return render(request, "sesame-modal-body.html", context)
