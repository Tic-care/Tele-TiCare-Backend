import cv2
import mediapipe as mp
import math 
import statistics
import numpy as np

# ------------------------------------  Frame Analysis
class Tic:  
    # face bounder indices 
    FACE_OVAL=[ 10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288, 397, 365, 379, 378, 400, 377, 152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234, 127, 162, 21, 54, 103,67, 109]
    # lips indices for Landmarks
    LIPS=[ 61, 146, 91, 181, 84, 17, 314, 405, 321, 375,291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95,185, 40, 39, 37,0 ,267 ,269 ,270 ,409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78 ]
    LOWER_LIPS =[61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95]
    UPPER_LIPS=[ 185, 40, 39, 37,0 ,267 ,269 ,270 ,409, 415, 310, 311, 312, 13, 82, 81, 42, 183, 78] 
    # Left eyes indices 
    LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385,384, 398 ]
    LEFT_EYE_LOWER =[ 362, 382, 381, 380, 374, 373, 390,249, ]
    LEFT_EYE_UPPER =[ 263, 466, 388, 387, 386, 385,384, 398 ]
    LEFT_EYEBROW =[ 336, 296, 334, 293, 300, 276, 283, 282, 295, 285 ]
    # right eyes indices
    RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ] 
    RIGHT_EYE_LOWER=[ 33, 7, 163, 144, 145, 153, 154, 155 ]  
    RIGHT_EYE_UPPER=[133, 173, 157, 158, 159, 160, 161 , 246 ]  
    RIGHT_EYEBROW=[ 70, 63, 105, 66, 107, 55, 65, 52, 53, 46 ]

    original_image=None
    results=None
    landmarks=None


    def __init__(self , image):
        self.original_image=image
        self.height, self.width, _ = self.original_image.shape
        # Initialize the MediaPipe FaceMesh solution
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        # Process the image to find face landmarks
        self.results = face_mesh.process(image)
        # Initialize mediapipe pose class.
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose()
        # Process the image.
        keypoints = pose.process(image)
        # Use lm and lmPose as representative of the following methods.
        self.lm = keypoints.pose_landmarks
        self.lmPose = mp_pose.PoseLandmark


    def updateImage(self,newImage):
        self.original_image=newImage

    def draw_indecies(self,list_indecies,color,output_image):
        for idx in list_indecies:
            landmark = self.landmarks.landmark[idx]
            height, width, _ = self.original_image.shape
            cx, cy = int(landmark.x * width), int(landmark.y * height)
            cv2.circle(output_image, (cx, cy), 1, color, -1)
        
    def draw_eye_indecies(self,):
        if self.results.multi_face_landmarks:
            # Get the first detected face
            self.landmarks = self.results.multi_face_landmarks[0]
            # Create an empty image to draw only the mouth landmarks
            eye_image = self.original_image.copy()
            # Draw indecies on image 
            self.draw_indecies(self.LEFT_EYE_UPPER,(0,0,255),eye_image)
            self.draw_indecies(self.LEFT_EYE_LOWER,(255,0,255),eye_image)    
            self.draw_indecies(self.RIGHT_EYE_UPPER,(0,0,255),eye_image)    
            self.draw_indecies(self.RIGHT_EYE_LOWER,(255,0,255),eye_image) 

            return eye_image
        else:
            return "no landmarks detected"

    def findDistance(self,p1, p2,color ,output_image):
        height, width, _ = self.original_image.shape
        x1, y1 = int(p1.x* width),int(p1.y* height)
        x2, y2 = int(p2.x* width),int(p2.y* height)
        cx, cy = int((x1 + x2) // 2), int((y1 + y2) // 2)

        # length = math.hypot(x2 - x1, y2 - y1)
        length=math.dist((p1.x, p1.y ), (p2.x, p2.y))
        # length=math.dist((x1, y1 ), (x2, y2))

        # draw Points 
        # cv2.circle(output_image, (x1, y1), 1, color, -1)
        # cv2.circle(output_image, (x2, y2), 1, color, -1)
        # cv2.circle(output_image, (cx, cy), 1, color, -1)
        # Draw Line
        # cv2.line(output_image, (x1, y1), (x2, y2), color, thickness=1)
        return length, output_image
    
    def findAngle(x1, y1, x2, y2):
        theta = math.acos((y2 -y1)*(-y1) / (math.sqrt((x2 - x1)**2 + (y2 - y1)**2) * y1))
        degree = int(180/math.pi)*theta
        return degree
           
    def calculate_eye_distances(self):
        if self.results.multi_face_landmarks:
            # Get the first detected face
            self.landmarks = self.results.multi_face_landmarks[0]
            # Create an empty image to draw only the mouth landmarks
            output_image = self.original_image.copy()
            # Left eye analysis
            leftUp   = self.landmarks.landmark[386]
            leftDown = self.landmarks.landmark[253]
            leftLeft = self.landmarks.landmark[362]
            leftRight =self.landmarks.landmark[263]
            leftlenghtVer,_ = self.findDistance(leftUp, leftDown,color=(255,255,0),output_image=output_image)
            leftlenghtHor,_ = self.findDistance(leftLeft, leftRight,color=(255,0,0),output_image=output_image)
            leftEyeRatio=leftlenghtVer/leftlenghtHor
            # Right eye analysis
            rightUp   = self.landmarks.landmark[159]
            rightDown = self.landmarks.landmark[23]
            rightLeft = self.landmarks.landmark[133]
            rightRight =self.landmarks.landmark[33]
            rightLenghtVer,_= self.findDistance(rightUp, rightDown,color=(255,255,0),output_image=output_image)
            rightLenghtHor,_ = self.findDistance(rightLeft, rightRight,color=(255,0,0),output_image=output_image)
            rightEyeRatio=rightLenghtVer/rightLenghtHor
            
            # All data
            data=(rightLenghtVer,rightLenghtHor,leftlenghtVer,leftlenghtHor)           
            return rightEyeRatio,leftEyeRatio,data ,output_image

        else:
            return "no landmarks detected"    

    def calculate_brow_distances(self):
        if self.results.multi_face_landmarks:
            # Get the first detected face
            self.landmarks = self.results.multi_face_landmarks[0]
            # Create an empty image to draw only the mouth landmarks
            output_image = self.original_image.copy()
            # Left eye analysis
            leftUp   = self.landmarks.landmark[295]
            leftDown = self.landmarks.landmark[258]
            leftLeft = self.landmarks.landmark[276]
            leftRight =self.landmarks.landmark[285]
            leftlenghtVer,_ = self.findDistance(leftUp, leftDown,color=(255,255,0),output_image=output_image)
            leftlenghtHor,_ = self.findDistance(leftLeft, leftRight,color=(255,0,0),output_image=output_image)
            leftEyeRatio=leftlenghtVer/leftlenghtHor
            # Right eye analysis
            rightUp   = self.landmarks.landmark[65]
            rightDown = self.landmarks.landmark[28]
            rightLeft = self.landmarks.landmark[55]
            rightRight =self.landmarks.landmark[46]
            rightLenghtVer,_= self.findDistance(rightUp, rightDown,color=(255,255,0),output_image=output_image)
            rightLenghtHor,_ = self.findDistance(rightLeft, rightRight,color=(255,0,0),output_image=output_image)
            rightEyeRatio=rightLenghtVer/rightLenghtHor
            
            # All data
            data=(rightLenghtVer,rightLenghtHor,leftlenghtVer,leftlenghtHor)           
            return rightEyeRatio,leftEyeRatio,data ,output_image

        else:
            return "no landmarks detected" 
        
    def calculate_mouth_distance(self):
        #up,down, left , right
        mouth_id={'up':0,'down':17,'left':291,'right':61}
        if self.results.multi_face_landmarks:
            # Get the first detected face
            self.landmarks = self.results.multi_face_landmarks[0]
            # Create an empty image to draw only the mouth landmarks
            output_image = self.original_image.copy()
            # Mouth analysis
            mouthUp    = self.landmarks.landmark[mouth_id['up']]
            mouthDown  = self.landmarks.landmark[mouth_id['down']]
            mouthLeft  = self.landmarks.landmark[mouth_id['left']]
            mouthRight = self.landmarks.landmark[mouth_id['right']]
            mouthVer,_ = self.findDistance(mouthUp, mouthDown,color=(255,255,0),output_image=output_image)
            mouthHor,_ = self.findDistance(mouthLeft, mouthRight,color=(255,0,0),output_image=output_image)
            mouthRatio = mouthVer / mouthHor
    
            # All data
            data=(mouthVer,mouthHor,mouthRatio)           
            return mouthRatio,data ,output_image

        else:
            return "no landmarks detected" 

    def calculate_neck(self):
     
        # Get the first detected face
        self.landmarks = self.results.multi_face_landmarks[0]
        # Create an empty image to draw only the mouth landmarks
        output_image = self.original_image.copy()
        # Left shoulder.
        l_shldr_x = int(self.lm.landmark[self.lmPose.LEFT_SHOULDER].x * self.width)
        l_shldr_y = int(self.lm.landmark[self.lmPose.LEFT_SHOULDER].y * self.height)
        # Right shoulderself.
        r_shldr_x = int(self.lm.landmark[self.lmPose.RIGHT_SHOULDER].x * self.width)
        r_shldr_y = int(self.lm.landmark[self.lmPose.RIGHT_SHOULDER].y * self.height)
        # Left earself.
        l_ear_x   = int(self.lm.landmark[self.lmPose.LEFT_EAR].x * self.width)
        l_ear_y   = int(self.lm.landmark[self.lmPose.LEFT_EAR].y * self.height) 
        # right ear.
        r_ear_x = int(self.lm.landmark[self.lmPose.RIGHT_EAR].x * self.width)
        r_ear_y = int(self.lm.landmark[self.lmPose.RIGHT_EAR].y * self.height)     
        # Calculate angles.
        neckL_inclination  = self.findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
        neckR_inclination  = self.findAngle(r_shldr_x, r_shldr_y, r_ear_x  , r_ear_y)
        NeckRatio=neckR_inclination/neckL_inclination
        data=(NeckRatio,neckR_inclination,neckL_inclination)
        return NeckRatio,data ,output_image
        
#--------------------------------------------------------- Video Analysis
class SpatialAnalysis(Tic):
    def __init__(self , Video_path):

        self.cap = cv2.VideoCapture(Video_path)
        self.frame_rate = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.frame_number = 0
        self.video_len=0
        # Intialize variables
        self.Rb=[]
        self.Lb=[]
        self.Re=[]
        self.Le=[]
        self.M =[]
        self.N=[]


    def oneSecProcessing(self):
        self.frame_number = 0
        # Intialize variables
        temp_Rb=[]
        temp_Lb=[]
        temp_Re=[]
        temp_Le=[]
        temp_M=[]
        temp_N=[]
        #video looping
        while True:   
            success, frame = self.cap.read()
            if not success:
                print("Done")
                break
            self.frame_number +=1

            # skip 10 frames
            if self.frame_number % 3 ==0:      
                # Start frame analysis
                tic_frame=Tic(frame)

                if tic_frame.results.multi_face_landmarks:
                    # landmarks = tic_frame.results.multi_face_landmarks[0]
                    e1,e2,len_data,dist_img=tic_frame.calculate_eye_distances()
                    tic_frame.updateImage(dist_img)
                    b1,b2,len_data,dist_img=tic_frame.calculate_brow_distances()
                    tic_frame.updateImage(dist_img)
                    m,len_data,dist_img=tic_frame.calculate_mouth_distance()
                    tic_frame.updateImage(dist_img)
                    n,len_data,dist_img=tic_frame.calculate_mouth_distance()
                    temp_Rb.append(b1)
                    temp_Lb.append(b2)
                    temp_Re.append(e1)
                    temp_Le.append(e2)
                    temp_M.append(m)
                    temp_N.append(n)

            #check end of a second
            if self.frame_number % self.frame_rate == 0: 
                # Calculate the mean per second
                self.Rb.append(statistics.mean(temp_Rb))
                self.Lb.append(statistics.mean(temp_Lb))
                self.Re.append(statistics.mean(temp_Re))
                self.Le.append(statistics.mean(temp_Le))
                self.M.append(statistics.mean(temp_M))
                self.N.append(statistics.mean(temp_N))
                #increment length
                self.video_len+=1


          
                # Intialize variables
                temp_Rb=[]
                temp_Lb=[]
                temp_Re=[]
                temp_Le=[]
                temp_M=[]
                temp_N=[]

        # return self.Rb, self.Lb, self.Re, self.Le , self.M
    
    def set_threshold(self, method ,thresholdMultiplier=[1,1,1,1,1,1,1]):

        if method == 1:
            self.TRB=statistics.mean(self.Rb)
            self.TLB=statistics.mean(self.Lb)
            self.TRE=statistics.mean(self.Re)
            self.TLE=statistics.mean(self.Le)
            self.TM=statistics.mean(self.M)
            self.TN=statistics.mean(self.N)

        elif method == 2:
            self.TRB=min(self.Rb) + 0.9 * (max(self.Rb) - min(self.Rb))
            self.TLB=min(self.Lb) + 0.9 * (max(self.Lb) - min(self.Lb))
            self.TRE=min(self.Re) + 0.9 * (max(self.Re) - min(self.Re))
            self.TLE=min(self.Le) + 0.9 * (max(self.Le) - min(self.Le))
            self.TM=min(self.M)   + 0.9 * (max(self.M) - min(self.M))
            self.TN=min(self.M)   + 0.9 * (max(self.N) - min(self.N))

        elif method == 3:
            self.TRB=statistics.mean(self.Rb) + thresholdMultiplier[0] * np.std(self.Rb)
            self.TLB=statistics.mean(self.Lb) + thresholdMultiplier[1] * np.std(self.Lb)
            self.TRE=statistics.mean(self.Re) + thresholdMultiplier[2] * np.std(self.Re)
            self.TLE=statistics.mean(self.Le) + thresholdMultiplier[3] * np.std(self.Rb)
            self.TM =statistics.mean(self.M)  + thresholdMultiplier[4] * np.std(self.M)
            self.TN =statistics.mean(self.N)  + thresholdMultiplier[5] * np.std(self.N)


    def detect_tics(self):

        self.set_threshold(method=3,thresholdMultiplier=[1,1,1,1,1,1])

        resultsPerSec=[]
        for idx in range(0,self.video_len):
            names=[]
            values=[]
            if(self.Rb[idx]>self.TRB):
                names.append('Rb')
                values.append(1)
            else:
                values.append(0)
                names.append('normal')

            if(self.Lb[idx]>self.TLB):
                names.append('Lb')
                values.append(1)
            else:
                values.append(0)
                names.append('normal') 
                   
            if(self.Re[idx]>self.TRE):
                names.append('Re')
                values.append(1)
            else:
                values.append(0)
                names.append('normal')

            if(self.Le[idx]>self.TLE):
                names.append('Re')
                values.append(1)
            else:
                values.append(0)
                names.append('normal')

            if(self.M[idx]>self.TM):
                names.append('M')
                values.append(1)
            else:
                values.append(0)
                names.append('normal') 

            if(self.N[idx]>self.TN):
                names.append('N')
                values.append(1)
            else:
                values.append(0)
                names.append('normal') 
            resultsPerSec.append(values)
        return resultsPerSec

