from deepface import DeepFace
import cv2
import numpy as np
from collections import Counter
from matplotlib import pyplot as plt
import seaborn as sns

class EmotionRecognation:
    def __init__(self, videos_paths) -> None:
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.imgs = []
        self.emotions = []
        self.videos_paths = videos_paths

    def has_face(self, img):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detecting faces in the image
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        # If faces are detected, return True; otherwise, return False
        return len(faces) > 0

    def read_video(self,path):
        self.imgs = []

        # Open the video file
        cam = cv2.VideoCapture(path)

        # Get the original frames per second (fps) of the video
        original_fps = cam.get(cv2.CAP_PROP_FPS)

        # Check if the video file was opened successfully
        if not cam.isOpened():
            print('Failed to open video file')
            return

        # Calculate the interval between frames to capture at 5 fps
        capture_interval = int(original_fps / 5)

        # Initialize the frame counter
        frame_counter = 0

        # Loop until the end of the video file
        while True:
            # Read the next frame of the video
            ret, frame = cam.read()

            # If the frame was read successfully, check the frame counter
            if ret:
                # Capture a frame every 'capture_interval' frames
                if frame_counter % capture_interval == 0:
                    self.imgs.append(frame)
                frame_counter += 1
            else:
                break

        # Release the video capture object and close all OpenCV windows
        cam.release()
        cv2.destroyAllWindows()

    def find_emotion(self):
        for i in range(len(self.imgs)):
            if self.has_face(self.imgs[i]):
                try:
                    self.emotions.append(DeepFace.analyze(
                        self.imgs[i])[0]['dominant_emotion'])
                except:
                    self.emotions.append('no face detected')
                

        all_no_face = all(
            emotion == 'none' for emotion in self.emotions)

        # Calculate the average emotion within this second
        if all_no_face:
            average_emotion = 'none'
        else:
            # print(self.emotions)
            values, counts = np.unique(self.emotions, return_counts=True)
            index = np.argmax(counts)
            average_emotion = values[index]

        return average_emotion
    
    def draw_emotion_chart(self, emotions_list):

        # Count the frequency of each emotion
        emotion_counts = Counter(emotions_list)

        # Create labels and sizes for the pie chart
        labels = emotion_counts.keys()
        sizes = emotion_counts.values()

        # Create the pie chart
        plt.figure(figsize=(10, 7))
        wedges, texts, autotexts = plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Paired"),
                                        textprops={'fontsize': 14,  'weight': "bold"}, pctdistance=0.75)  # Adjust fontsize as needed

        # Adjusting fontsize and properties of autopct
        plt.setp(autotexts, size=12, weight="bold")
        # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.axis('equal')

        # Save the pie chart as an image
        plt.savefig('uploads/emotion_pie_chart.png')

        return 'uploads/emotion_pie_chart.png'

    # def get_emotion_in_video(self):
    #     self.read_video()
    #     avg_emotion = self.find_emotion()
    #     print(f"The average Emotion is {avg_emotion}************************")
    
    def get_emotions(self):
        avg_emotions=[]
        for video in self.videos_paths:
            print(video)
            self.read_video(video)
            avg_emotions.append(self.find_emotion())
        print(f'avg_emotions {avg_emotions}')
        path = self.draw_emotion_chart(avg_emotions)
        return avg_emotions, path
        

# emotion = EmotionRecognation(['downloaded_videos/subject1_video13.mp4'])
# emotion.get_emotion_in_video()
