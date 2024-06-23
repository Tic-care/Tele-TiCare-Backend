import pyrebase


def stream_handler(message):
    # Process the data change (e.g., print, trigger actions)
    print(f"Event type: {message['event']}")
    print(f"Data: {message['data']}")
    print(message)

class database_connection():
    def __init__(self, local_download_path, local_upload_path) -> None:
        self.db = None
        self.storage = None
        self.local_download_path = local_download_path
        self.local_upload_path = local_upload_path
        self.users = None 
        self.firebase= None
        self.config = None

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


    # def init_storage(self):
        

    def upload_file(self, upload_video_name, storing_path):
        self.storage.child(f"{storing_path}").put(
            f"{self.local_upload_path}/{upload_video_name}")
        
    def download_file(self, firebase_file_path, download_file_name):
        self.storage.child().download(path=firebase_file_path,
                                        filename=f"{self.local_download_path}/{download_file_name}")

    

    def start_stream(self, streamed_database):
        self.stream = self.db.child(f"{streamed_database}").stream(
            stream_handler=stream_handler)

    def stop_streaming(self):
        self.stream.close()



# config = {
#     "apiKey": "AIzaSyCwO-qOsE-aav2z6eHrHbmbOG_UYLUiUMY",
#     "authDomain": "ticare-c6d15.firebaseapp.com",
#     "databaseURL": "https://ticare-c6d15-default-rtdb.firebaseio.com",
#     "storageBucket": "ticare-c6d15.appspot.com",
#     "serviceAccount": "ticare-c6d15-firebase-adminsdk-4qya1-a663792323.json"
# }

# firebase = pyrebase.initialize_app(config)
# db = firebase.database()

# users =db.child("users").get()

# print(users.key())
