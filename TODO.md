# ToDos

* [X] [Call celery task on save, the save way](https://stackoverflow.com/a/54313701)
* [X] add new video status (downloading)
* [X] add display of emtpy thumbnail for downloading videos
* [X] show all videos even if they are not finished
* [X] add abiltiy to delete videos
* [X] show original title and description in detail view
* [X] create view to display subscription link
* [X] add speed control to player
* [X] make video div smaller, CSS not working
* [ ] use html video tag instead of video.js?
* [ ] skip forward/backwards by double tapping on video
* [ ] better looking audio player
* [ ] better looking video playing page
* [X] fix pagination in list view
* [ ] replace url with path/re_path due to url deprecation
* [X] fix sending confirmation email
* [ ] add ability to switch between self hosted mail and [anymail](https://anymail.dev/en/stable/)
* [ ] add ability to set initial admin password from env
* [ ] add Helm chart
* [ ] option to retry download
* [ ] error handling on video download
* [ ] add search
* [X] add link to admin interface for superusers
* [X] add doc how to reset admin password
* [ ] add ability to download playlists
  * viddlws playlist vs remote playlist?
  * remote playlist - should it be possible to remove items/resort items?
  * remote playlist - auto download new videos from remote? how to notify user about new items?
  * should playlists be subscribal? what happens if the playlist is resorted?
* [ ] subscribe to channel
  * only auto download videos with regex on original title
  * how to notify user about new downloads?
* [X] show used and free space on the mount point used for downloads
  * https://stackoverflow.com/a/39799743
  * https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
  * [X] show as values
  * [X] show as small graph
* [ ] add the possibility to make certain video/audio content publicly available without need to be logged in?
