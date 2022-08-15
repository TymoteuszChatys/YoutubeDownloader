from pytube import YouTube
from pytube import Channel
import sqlite3
import os
import re

def alter_title(title):
    title = re.sub(r'[^A-Za-z0-9 ]+', '', title)
    return title

def alter_channel_name(channel_name):
    channel_name = re.sub(r'[^A-Za-z0-9 ]+', '', channel_name)
    channel_name = channel_name.replace(" ","_")
    return channel_name

def populate_videos(current_channel,number_of_videos_to_check,db_connection,db_cursor):

    print("------------------------------------------------------------")
    print(f'Checking for new videos by: {current_channel.channel_name}')

    video_count = 0
    for video in current_channel.videos:
        video_in_database = False
        try:
            a = db_cursor.execute(f"SELECT * FROM Videos WHERE id = '{video.video_id}'")
            len(a.fetchone())
            video_in_database = True
        except:
            None

        if video_in_database == False:
            try:
                db_cursor.execute(f"INSERT INTO Videos VALUES ('{video.author}','{video.video_id}','{video.watch_url}','{alter_title(video.title)}',{video.length},0,'')")
                db_connection.commit()

                print(f"-NEW VIDEO- {video.title}")
                
            except:
                print(video.title)
        #
        video_count += 1

        if video_count == number_of_videos_to_check:
            break

    print("------------------------------------------------------------")

def populate_db(db_connection,db_cursor):
    channels = []
	
    #add your channels here
    channels.append("https://www.youtube.com/c/Coffeezilla")
    
    #Look at n past videos
    n = 5
    
    for channel in channels:
        current_channel = Channel(channel)
        populate_videos(current_channel,n,db_connection,db_cursor)


def download_videos(db_connection,db_cursor):
    testing = False

    for row in db_cursor.execute(f"SELECT * FROM Videos WHERE Downloaded = 0"):
        if testing == False:
            try:
                channel = alter_channel_name(row[0])
                id = row[1]
                link = row[2]

                dir_path = os.path.dirname(os.path.realpath(__file__))
                path = f"/videos/{channel}/"
                path_exist = os.path.exists(dir_path+path)

                if not path_exist:
                    #Create a new directory if it does not exist
                    os.makedirs(dir_path+path)
                    print(f"New channel added - {channel}")

                video_stream = YouTube(link).streams.get_highest_resolution()
                video_stream.download(dir_path+path)

                sql = f"UPDATE Videos SET Downloaded = 1 WHERE id = '{id}'"

                print(f"Video with video id {id} from {channel} downloaded.")

                db_connection.cursor().execute(sql)
                db_connection.commit()
            except:
                print(f"ERROR downloading video - {link}")
        else:
            channel = alter_channel_name(row[0])
            id = row[1]
            link = row[2]

            dir_path = os.path.dirname(os.path.realpath(__file__))
            path = f"/videos/{channel}/"
            path_exist = os.path.exists(dir_path+path)

            if not path_exist:
                #Create a new directory if it does not exist
                os.makedirs(dir_path+path)
                print(f"New channel added - {channel}")

            video_stream = YouTube(link).streams.get_highest_resolution()
            video_stream.download(dir_path+path)

            sql = f"UPDATE Videos SET Downloaded = 1 WHERE id = '{id}'"

            print(f"Video with video id {id} from {channel} downloaded.")

            db_connection.cursor().execute(sql)
            db_connection.commit()

db_connection = sqlite3.connect("YT.db")
db_cursor = db_connection.cursor()

populate_db(db_connection,db_cursor)
download_videos(db_connection,db_cursor)
