# import emotion_recognation as emotion_rec
from emotion_recognation import EmotionRecognation
# import temporal_detection as temp_detect
import TemporalMethod as temp_detect
from spatialAnalysisv2 import SpatialAnalysis
from TemporalMethod import TemporalDetection, ModifiedSlowFast, PackPathway

def video_process(filePath):
    input_video = SpatialAnalysis(filePath)
    print("Areas Processing")
    input_video.oneSecProcessing()
    print("Done Processing")
    results = input_video.detect_tics()
    # Print all in results
    for idx, result in enumerate(results):
        print(idx, result)
    print("video_len", input_video.video_len)
    return results


def detect_areas(results, TicsSec=[[0, 2]], ticThreshold=2):
    finalResult = []
    names = ['right brow', 'left brow',
             'right eye', 'left eye', 'mouth', 'Neck']

    #  results in specified intervals
    for idx, interval in enumerate(TicsSec):
        print("Tic:", idx+1, ' interval', interval)
        templist = []
        counter = [0, 0, 0, 0, 0, 0]
        areasPerSec = []
        # loops in interval example [0,2] -->0,1,2
        for indx in range(interval[0], interval[1]+1):
            print('sec', indx)
            templist = results[indx]
            # loops in areas result example [0,0,0,1,0,1] where 0-> no tics in this area , 1 -> potential tic
            for area_idx in range(0, len(templist)):
                counter[area_idx] = counter[area_idx]+templist[area_idx]
                if counter[area_idx] >= ticThreshold:
                    print(names[area_idx])
                    areasPerSec.append(names[area_idx])
        print(counter)
        print(areasPerSec)
        finalResult.append(areasPerSec)

    return finalResult









class TicDetection():
    def __init__(self, file_path, upload_path) -> None:
        self.file_path = file_path
        self.upload_path = upload_path
        self.final_detect = None

    def detect_tic(self):
        # detect_tics = temp_detect.TemporalDetection(
        #     "downloaded_videos/subject1_video9.mp4", "upload_videos")
        detect_tics = TemporalDetection(
            self.file_path, self.upload_path)
        temporals = detect_tics.Temporal_Detection()
        print("Temporal Done!!!!")
        # {'clips_in_ranges': clips_in_ranges, "output_path": self.output_dir,
        #     'tics_count': tics_count, 'clips': clips, 'predictions': preds}
        body_parts=[]
        avg_emotion = []
        print(temporals)
        results = video_process(self.file_path)
        print("results calculated")
        for i, interval in enumerate(temporals['clips_in_ranges']):   
            print(interval)
            body_parts.append(detect_areas(
                results, TicsSec=interval,  ticThreshold=1))
            print("one clip body part!!!!")
            emotion = EmotionRecognation(temporals['output_path'][i])
            avg_emotion.append(emotion.get_emotion_in_video())
            print("one clip emotions!!!!")

        print("Spatial & Emotions Done!!!!")
        # for video in temporals['output_path']:
        #     emotion = EmotionRecognation(video)
        #     avg_emotion.append(emotion.get_emotion_in_video())

        temporals['body_parts'] = body_parts
        temporals['emotions'] = avg_emotion
        print(temporals)
        
print("***")
tics = TicDetection("downloaded_videos/subject1_video1.mp4", "upload_videos")
tics.detect_tic()

# temporals = temp_detect.TemporalDetection("downloaded_videos/subject1_video9.mp4", "upload_videos")
