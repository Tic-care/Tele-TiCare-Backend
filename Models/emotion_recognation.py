from deepface import DeepFace
import cv2
import numpy as np


class EmotionRecognation:
    def __init__(self, video_path) -> None:
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.imgs = []
        self.emotions = []
        self.video_path = video_path

    def has_face(self, img):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detecting faces in the image
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

        # If faces are detected, return True; otherwise, return False
        return len(faces) > 0

    def read_video(self):
        # Open the video file
        cam = cv2.VideoCapture(self.video_path)

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
                self.emotions.append(DeepFace.analyze(
                    self.imgs[i])[0]['dominant_emotion'])

        all_no_face = all(
            emotion == 'no face detected' for emotion in self.emotions)

        # Calculate the average emotion within this second
        if all_no_face:
            average_emotion = 'no face detected'
        else:
            values, counts = np.unique(self.emotions, return_counts=True)
            index = np.argmax(counts)
            average_emotion = values[index]

        return average_emotion

    def get_emotion_in_video(self):
        images = self.read_video()
        avg_emotion = self.find_emotion()
        print(f"The average Emotion is {avg_emotion}************************")


# emotion = EmotionRecognation('videos/Untitled video - Made with Clipchamp (4).mp4')
# emotion.get_emotion_in_video()
