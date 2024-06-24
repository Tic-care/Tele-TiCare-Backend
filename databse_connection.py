import pyrebase


# flag = True

# def stream_handler(message):
#     if flag:
#         flag = False 
#         return
#     # Process the data change (e.g., print, trigger actions)
#     print("*********************************************************")
#     print(f"Event type: {message['event']}")
#     print(f"Data: {message['data']}")
#     # print(message)

class database_connection():
    def __init__(self, local_download_path, local_upload_path) -> None:
        self.db = None
        self.storage = None
        self.local_download_path = local_download_path
        self.local_upload_path = local_upload_path
        self.users = None 
        self.firebase= None
        self.config = None
        self.flag = True

    def initialize(self):
        self.config = {
            "apiKey": "AIzaSyCwO-qOsE-aav2z6eHrHbmbOG_UYLUiUMY",
            "authDomain": "ticare-c6d15.firebaseapp.com",
            "databaseURL": "https://ticare-c6d15-default-rtdb.firebaseio.com",
            "storageBucket": "ticare-c6d15.appspot.com",
            "serviceAccount": "ticare-c6d15-firebase-adminsdk-4qya1-a663792323.json"
        }

        self.firebase = pyrebase.initialize_app(self.config)
        self.db = self.firebase.database()
        self.storage = self.firebase.storage()
        self.users = self.db.child("users").get()
        
    def upload_file(self, upload_video_name, storing_path):
        self.storage.child(f"{storing_path}").put(
            f"{self.local_upload_path}/{upload_video_name}")
        
        
    def download_file(self, firebase_file_path, download_file_name):
        self.storage.child().download(path=firebase_file_path,
                                        filename=f"{self.local_download_path}/{download_file_name}")

    def get_url(self,file_path):
        print(file_path)
        file = self.storage.child(file_path)
        return file.get_url(None)

    def start_stream(self, streamed_database):
        self.stream = self.db.child(f"{streamed_database}").stream(
            stream_handler=lambda message: self.stream_handler(message))

    def stop_streaming(self):
        self.stream.close()

    def push_data(self, path, data):
        self.db.child(f"{path}").push(data)

    def download_video(self, user_id, video_id):
        self.download_file(
            f"/videos/{user_id}/recorded_{video_id}.webm", f'{video_id}.webm')
        print(f"Video {video_id} of user {user_id} successfully downloaded!")
        
    def upload_video(self, local_video_name, user_id, video_id, video_no, video_type='webm'):
        self.upload_file(
            local_video_name, f"snippets/{user_id}/{video_id}/{video_no}.{video_type}")
        return self.get_url(f"snippets/{user_id}/{video_id}/{video_no}.{video_type}")


    def stream_handler(self, message):
        if self.flag:
            self.flag = False
            return
        # Process the data change (e.g., print, trigger actions)
        print("*********************************************************")
        print(f"Event type: {message['event']}")
        print(f"Data: {message['data']}")
        print(f"Path: {message['path']}")
        print(message)
        if (message['event'] == 'patch'):
            print(f"{message['path'].split('/')[1]}")
            user_id = message['path'].split('/')[1]
            video_id = list(message['data'].keys())[0]
            self.download_video(user_id, video_id)
            ####call the functions########

            video_path = f"users/{user_id}/videos/{video_id}/reports/detectedClips"
            self.db.child(video_path).update({"reports": {}})


            vid_names=["1.webm", "2.webm"]
            captions = ["time1->2", "time11->12"]
            
            for i, vid in enumerate(vid_names):
                link= self.upload_video(vid, user_id, video_id, i)
                self.db.child(video_path).update({"vid": {}})
                vid_path = video_path + f"/Clip{i}"
                print(vid_path)
                report_data = {
                    "caption": captions[i],
                    "link": link
                }

                # Update the "report" key with the actual data
                self.db.child(vid_path).update(report_data)
                self.flag = True




        # if input("Stop Streaming?") == "0":
        #     self.stop_streaming()


































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
