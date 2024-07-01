import pyrebase
from tic_detection import TicDetection



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
        self.uid= None
        self.vid= None

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
        
    def upload_file(self, upload_file_name, storing_path):
        self.storage.child(f"{storing_path}").put(
            f"{self.local_upload_path}/{upload_file_name}")
        
        
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



    def unpack_results_dict(self, results_dict, video_db_path, session_db_path):


        



        for i, vid in enumerate(results_dict['output_path']):
            link= self.upload_video(vid, self.uid, self.vid, i+1)
            visual_link= self.upload_video(results_dict['visuals_paths'][i], self.uid, self.vid, f"visual{i+1}")
            # self.db.child(video_db_path).update({"vid": {}})  #does this do anything????
            vid_path = video_db_path + f"/Clip{i}"
            print(vid_path)

            #### Handle if the tic is in the same second, no body parts 
            caption = f"Interval from second {results_dict['clips_in_ranges'][i][0]} 
                        to second {results_dict['clips_in_ranges'][i][1]}, Body Part affected {results_dict['body_parts'][i]},
                        Dominant Emotion {results_dict['emotions'][i]}"
            report_data = {
                "caption": caption,
                "link": link, 
                "visual_link": visual_link
            }

            # Update the "report" key with the actual data
            self.db.child(vid_path).update(report_data)
            
            
        print("Uploading Clips Done!")

        self.upload_file(results_dict['bodyPartsHistogram'],
                            f"reports/{self.uid}/{self.vid}/{results_dict['bodyPartsHistogram'].split('/')[-1]}")
        body_parts_histogram_url = self.get_url(
            f"reports/{self.uid}/{self.vid}/{results_dict['bodyPartsHistogram'].split('/')[-1]}")
        
        self.upload_file(results_dict['durationHistogram'],
                            f"reports/{self.uid}/{self.vid}/{results_dict['durationHistogram'].split('/')[-1]}")
        duration_histogram_url = self.get_url(
            f"reports/{self.uid}/{self.vid}/{results_dict['durationHistogram'].split('/')[-1]}")
        
        self.upload_file(results_dict['emotions_chart'],
                            f"reports/{self.uid}/{self.vid}/{results_dict['emotions_chart'].split('/')[-1]}")
        emotion_chart_url = self.get_url(
            f"reports/{self.uid}/{self.vid}/{results_dict['emotions_chart'].split('/')[-1]}")
        
        session_data = {
                # "aiComment": results_dict['aiComment'],
                "bodyPartsHistogram": body_parts_histogram_url,
                "durationHistogram": duration_histogram_url,
                "emotions_chart" : emotion_chart_url,
                "numOfBodyParts": results_dict['numOfBodyParts'],
                "sessionLength": f"{results_dict['sessionLength']} second",
                "ticsCount": results_dict['ticsCount'],
                "ticsDuration": results_dict['ticsDuration'],
                "ticsIntensity": results_dict['ticsIntensity']

            }
        self.db.child(session_db_path).update(session_data)


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
        if (message['event'] == 'put' and message['data'] != None):
            print(f"{message['path'].split('/')[1]}")
            self.uid = message['path'].split('/')[1]
            self.vid = message['data']['id']
            self.download_video(self.uid, self.vid)


            

            video_db_path = f"users/{self.uid}/videos/{self.vid}/reports/detectedClips"
            session_db_path = f"users/{self.uid}/videos/{self.vid}/reports/sessionAnalysis"



            tic_detection = TicDetection(
                f"{self.local_download_path}/{self.vid}.webm", self.local_upload_path)
            print("Starting Tic Detection")
            results_dict = tic_detection.detect_tic()
            print("Finished Tic Detection")
            print(results_dict)

            self.unpack_results_dict(results_dict,video_db_path,session_db_path)
            


            self.flag = True
            
            






















# {
#         # 'clips_in_ranges': [[9, 9], [11, 11], [13, 16], [19, 19], [22, 22], [28, 29], [32, 32], [37, 40], [48, 48], [50, 50], [53, 53]], 
#         #  'output_path': ['uploads\\subject1_video1_1min_clip_1.mp4', 'uploads\\subject1_video1_1min_clip_2.mp4', 'uploads\\subject1_video1_1min_clip_3.mp4', 'uploads\\subject1_video1_1min_clip_4.mp4', 'uploads\\subject1_video1_1min_clip_5.mp4', 'uploads\\subject1_video1_1min_clip_6.mp4', 'uploads\\subject1_video1_1min_clip_7.mp4', 'uploads\\subject1_video1_1min_clip_8.mp4', 'uploads\\subject1_video1_1min_clip_9.mp4', 'uploads\\subject1_video1_1min_clip_10.mp4', 'uploads\\subject1_video1_1min_clip_11.mp4'],
#         #  'ticsDuration': 18, 
#         #  'sessionLength': 61.12, 
#         #  'ticsCount': 11, 
#         #  'ticsIntensity': 0.29450261780104714, 
#         #  'body_parts': [[], [], [], [], [], [], [], ['right brow'], [], [], []], 
#         #  'visuals_paths': ['uploads/Visuals/clip1.mp4', 'uploads/Visuals/clip2.mp4', 'uploads/Visuals/clip3.mp4', 'uploads/Visuals/clip4.mp4', 'uploads/Visuals/clip5.mp4', 'uploads/Visuals/clip6.mp4', 'uploads/Visuals/clip7.mp4', 'uploads/Visuals/clip8.mp4', 'uploads/Visuals/clip9.mp4', 'uploads/Visuals/clip10.mp4', 'uploads/Visuals/clip11.mp4'], 'emotions': ['fear', 'fear', 'fear', 'fear', 'sad', 'fear', 'sad', 'sad', 'sad', 'sad', 'sad'], 
#         #  'emotions_chart': 'uploads/emotion_pie_chart.png', 
#         #  'durationHistogram': 'uploads/histogram_durations.png', 
#         #  'bodyPartsHistogram': 'uploads/histogram_body_parts.png'
#          }










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
