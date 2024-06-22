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
db = firebase.database()

storage = firebase.storage()



# videos_storage = storage.child("videos")
# storage.child("trail/2.mp4").download("download","downloaded.mp4")
# url = storage.child(
#     "trail/2.mp4").get_url(token="81c84325-982a-48eb-88a9-27e18337568a")
# print(url)

# storage.child("trail").put("t.jpg")



# We store the file in local_img_dir, which is .jpg

# fireb_upload = storage.child("trail/img.jpg").put("t.jpg")

# storage.child("trail/2.mp4").delete("trail/2.mp4", None)


# storage.child(
#     "trail/img.jpg").download(path="download", filename="img1.jpg")
# print(storage.list_files())
# filename = "it.jpg"
# path="img/"
# download_path = os.path.join(path, filename)



# print(fireb_upload)
# print("Test image saved to FireBase Storage.")


users = db.child("users").get()
print(users.key())
local_download_path="downloaded_videos"
for user in users.each():
    print("***********************************")
    print(user.key())  # Morty
    videos = user.val()["videos"]
    print(type(videos))
    if videos:
        for video_name, video_data in videos.items():
            print("/////////////////////////////////////////")
            # print(video_data)
            # video = videos_storage.child(f"{user.key()}").child(
            #     f"recorded_{video_data['id']}.webm")
            firebase_storage_path = f"videos/{user.key()}/recorded_{video_data['id']}.webm"
            
            storage.child().download(path=firebase_storage_path,filename= f"{local_download_path}/{video_data['id']}.webm")
            # print(video)
            # video.download("download",f"{video_data['id']}.webm")
            # urllib.request.urlretrieve(video_data['url'], f'video_{video_name}.webm')
    
    # print(videos)  # {name": "Mortimer 'Morty' Smith"}




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
