===========
INTODUCTION
===========


This python script looks at youtube channels and downloads the last 'n' new videos into the
videos folder. If you already have the video downloaded, it will not download again.
Sometimes an error occurs, there is no known solution, however I have found that errored videos
do end up downloading when the script is ran at a later time (sometimes even a week later).
If an error does occur, the script will simply skip the video and try to redownload it the next
time you run it.

============
REQUIREMENTS
============

Please make sure you have a videos folder in the same directory as YTDownload.py
You also must have the YT.db file in the same directory.

You must install the pytube package for python.
You can do this with pip: "pip install pytube"

==========
HOW TO USE 
==========

edit the populate_db() function in the python script to add the channels that you want.
you can also set 'n' - the number of past videos to download here to.
