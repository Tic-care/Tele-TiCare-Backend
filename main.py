import os
import pyrebase
# import urllib.request
import databse_connection as db

database = db.database_connection(
    local_download_path="downloaded_videos", local_upload_path="upload_videos")

database.initialize()

users = database.users




# print(users.key())
# local_download_path="downloaded_videos"
# for user in users.each():
#     print("***********************************")
#     print(user.key())  # Morty
#     videos = user.val()["videos"]
#     print(type(videos))
#     if videos:
#         for video_name, video_data in videos.items():
#             print("/////////////////////////////////////////")
#             print(video_name)

#             firebase_storage_path = f"videos/{user.key()}/recorded_{video_data['id']}.webm"
#             database.download_file(firebase_storage_path, f"{video_data['id']}.webm")
            
# database.upload_file(
#     "1718899391908.webm", "photos/it.webm")
# database.download_file("photos/1718899391908.mp4", "vid.webm")
            
    


