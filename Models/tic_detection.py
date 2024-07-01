# import emotion_recognation as emotion_rec
from collections import Counter
from emotion_recognation import EmotionRecognation
# import temporal_detection as temp_detect
import TemporalMethod as temp_detect
from spatialAnalysisv2 import SpatialAnalysis ,Visulas,video_process,detect_areas
from TemporalMethod import TemporalDetection, ModifiedSlowFast, PackPathway
import seaborn as sns
import matplotlib.pyplot as plt



def draw_intervals_histogram(time_intervals, save_path):

    print(time_intervals)
    # Calculate durations
    durations = [end - start + 1 for start, end in time_intervals]
    print(durations)

    # Set the Seaborn color palette
    sns.set_palette("pastel")

    # Create a histogram of the durations
    plt.figure(figsize=(8, 6))
    sns.histplot(durations, kde=False, bins=len(
        durations), color=sns.color_palette()[2])

    # Set labels and title
    plt.xlabel('Duration')
    plt.ylabel('Frequency')
    plt.title('Histogram of Durations')

    # Save the figure as an image
    plt.savefig(save_path)

def flatten(lst):
    for item in lst:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

def draw_body_parts_histogram(body_parts, save_path):
    # Flatten the list
    flat_list = list(flatten(body_parts))

    # Count the frequency of each facial body part
    parts_count = Counter(flat_list)

    # Separate the parts and their counts for plotting
    parts = list(parts_count.keys())
    counts = list(parts_count.values())

    # Create a bar chart (histogram) of the facial body parts
    fig, ax = plt.subplots()
    ax.bar(parts, counts, color='skyblue', edgecolor='black')

    # Add title and labels
    ax.set_title('Histogram of Facial Body Parts')
    ax.set_xlabel('Facial Body Part')
    ax.set_ylabel('Frequency')

    # Save the figure as an image
    plt.savefig(save_path)
    return len(parts)



class TicDetection():
    def __init__(self, file_path, upload_path) -> None:
        self.file_path = file_path
        self.upload_path = upload_path
        self.final_detect = None


    def detect_tic(self):

        detect_tics = TemporalDetection(
            self.file_path, self.upload_path)
        result_dict = detect_tics.Temporal_Detection()
        print("Temporal Done!!!!")
        print(result_dict) 

        # {'clips_in_ranges': clips_in_ranges, "output_path": self.output_dir,
        #     'ticsDuration': tics_count, 'clips': clips, 'predictions': preds}

                # session_data = {
                # # "aiComment": results_dict['aiComment'],
                # # "bodyPartsHistogram": body_parts_histogram_url,
                # # "durationHistogram": duration_histogram_url,                                                
                # # "emotions_chart" : emotion_chart_url,                                                       ###DONE
                # "numOfBodyParts": results_dict['output_path'],                                         
                # "sessionLength": results_dict['sessionLength'],                                               ###Done
                # "ticsCount": results_dict['ticsCount'],                                                       ###DONE
                # "ticsDuration": results_dict['ticsDuration'],                                                   ###DONE
                # "ticsIntensity": int(results_dict['ticsCount'])/float(results_dict['sessionLength'])          ###Done
                # }

        # print(result_dict['sessionLength'], type(result_dict['sessionLength']))
        result_dict['ticsCount'] = len(result_dict['output_path'])
        result_dict['ticsIntensity'] = float(result_dict['ticsDuration'])/float(result_dict['sessionLength'])
        # print(result_dict['ticsIntensity'])

        thresholds,results = video_process(self.file_path)
        print("results calculated")
        body_parts = detect_areas(results, TicsSec=result_dict['clips_in_ranges'],  ticThreshold=1)
        print(f"result_dict: {result_dict['clips_in_ranges']}")
        result_dict['body_parts'] = body_parts

        visuals_paths=[]
        for i,path in enumerate(result_dict['output_path']):
            visuals_path=f"uploads/Visuals/clip{i+1}.mp4"
            visuals_paths.append(visuals_path)
            Video_visuals=Visulas(inputVideoPath=path,outputVideoPath=visuals_path,thresholds=thresholds)
            Video_visuals.get_visuals()
        result_dict['visuals_paths']=visuals_paths

        emotion = EmotionRecognation(result_dict['output_path'])
        emotions, emotion_chart_path = emotion.get_emotions()
        result_dict['emotions'] = emotions
        result_dict['emotions_chart'] = emotion_chart_path

        intervals_hist_path = 'uploads/histogram_durations.png'
        draw_intervals_histogram(result_dict['clips_in_ranges'], intervals_hist_path)
        result_dict['durationHistogram'] = intervals_hist_path

        body_parts_hist_path = 'uploads/histogram_body_parts.png'
        no_body_parts = draw_body_parts_histogram(result_dict['body_parts'], body_parts_hist_path)
        result_dict['bodyPartsHistogram'] = body_parts_hist_path
        result_dict['numOfBodyParts'] = no_body_parts




        for i,interval in enumerate(result_dict['clips_in_ranges']):

            result_dict['clips_in_ranges'][i][1]+=1


        
        
        print(result_dict)
        return result_dict
        
print("***")
tics = TicDetection("downloaded_videos/subject1_video1_1min.mp4", "uploads")
tics.detect_tic()

# temporals = temp_detect.TemporalDetection("downloaded_videos/subject1_video9.mp4", "uploads")
