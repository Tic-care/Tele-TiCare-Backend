import os
import pyrebase
# import urllib.request

config = {
    "apiKey": "AIzaSyCwO-qOsE-aav2z6eHrHbmbOG_UYLUiUMY",
    "authDomain": "ticare-c6d15.firebaseapp.com",
    "databaseURL": "https://ticare-c6d15-default-rtdb.firebaseio.com",
    "storageBucket": "ticare-c6d15.appspot.com",
    "serviceAccount": "config.json"
}





firebase = pyrebase.initialize_app(config)
# db = firebase.database()

storage = firebase.storage()
# videos_storage = storage.child("videos")
# storage.child("trail/2.mp4").download("download","downloaded.mp4")
# url = storage.child(
#     "trail/2.mp4").get_url(token="81c84325-982a-48eb-88a9-27e18337568a")
# print(url)

# storage.child("trail").put("t.jpg")
# users = db.child("users").get()
# print(users.key())


# We store the file in local_img_dir, which is .jpg

# fireb_upload = storage.child("photos/img.jpg").put("t.jpg")

storage.child("trail/2.mp4").download(filename="download/it.mp4",
                                         path="download/")


# filename = "it.jpg"
# path="img/"
# download_path = os.path.join(path, filename)

# if os.path.exists(download_path):
#     print(f"File already exists: {download_path}")
#     # Optionally, generate a unique filename here
# else:
#     fireb_upload = storage.child("img.jpg").download(
#         filename=filename, path=path)
#     print("Download successful!")



# print(fireb_upload)
# print("Test image saved to FireBase Storage.")

# for user in users.each():
#     print("***********************************")
#     print(user.key())  # Morty
#     videos = user.val()["videos"]
#     print(type(videos))
#     if videos:
#         for video_name, video_data in videos.items():
#             print("/////////////////////////////////////////")
#             # print(video_data)
#             # video = videos_storage.child(f"{user.key()}").child(
#             #     f"recorded_{video_data['id']}.webm")
#             storage.child(
#                 f"videos/{user.key()}/recorded_{video_data['id']}.webm").download("download", f"{video_data['id']}.webm")
#             # print(video)
#             # video.download("download",f"{video_data['id']}.webm")
#             # urllib.request.urlretrieve(video_data['url'], f'video_{video_name}.webm')
    
#     # print(videos)  # {name": "Mortimer 'Morty' Smith"}




# def stream_handler(message):
#     # Process the data change (e.g., print, trigger actions)
#     print(f"Event type: {message['event']}")
#     print(f"Data: {message['data']}")
#     print(message)


# # Listen for changes at a specific path
# my_stream = db.child("clips").stream(stream_handler=stream_handler)

# # Keep the stream alive (replace with your main application loop)
# while True:
#     pass
