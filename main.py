import os
import pyrebase
# import urllib.request
import databse_connection as db




database = db.database_connection(
    local_download_path="downloaded_videos", local_upload_path="uploads")

database.initialize()

users = database.users

database.start_stream("users")


    


