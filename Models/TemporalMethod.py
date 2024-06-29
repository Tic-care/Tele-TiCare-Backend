# Run pip install fvcore to install this library
#Then run pip install av after the first library installation
import cv2
import tensorflow as tf
import numpy as np
import pandas as pd
from typing import Dict
import json
import urllib
# import torchvision
# import torchvision.transforms as transforms
import torch
import os
#To install certain libraries that will be used in pytorchvideo
MODEL = torch.hub.load('facebookresearch/pytorchvideo', 'slowfast_r50', pretrained=True)
import torchvision.io as io
from sklearn.preprocessing import StandardScaler
from torchvision.transforms import Compose, Lambda
from torchvision.transforms._transforms_video import (
    CenterCropVideo,
    NormalizeVideo,
)
from pytorchvideo.data.encoded_video import EncodedVideo # type: ignore
from pytorchvideo.transforms import ( # type: ignore
    ApplyTransformToKey,
    ShortSideScale,
    UniformTemporalSubsample,
    UniformCropVideo
)
import torch.nn as nn
from pytorchvideo.models import slowfast # type: ignore
#Import this class to get PyTorch be familiar with the class and the structure of the model
class ModifiedSlowFast(nn.Module):
    def __init__(self, original_model):
        super(ModifiedSlowFast, self).__init__()

        # Copy all layers except the head from the original model
        self.features = nn.Sequential(*list(original_model.blocks.children())[:-1])
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))  # Global average pooling

    def forward(self, x):
        # Forward pass through the modified SlowFast model
        x = self.features(x)
        x = self.avgpool(x)
        return x

side_size = 256
mean = [0.45, 0.45, 0.45]
std = [0.225, 0.225, 0.225]
crop_size = 256
num_frames = 32
sampling_rate = 1
frames_per_second = 30
slowfast_alpha = 4
num_clips = 10
num_crops = 3

class PackPathway(torch.nn.Module):
    """
    Transform for converting video frames as a list of tensors.
    """
    def __init__(self):
        super().__init__()

    def forward(self, frames: torch.Tensor):
        fast_pathway = frames
        # Perform temporal sampling from the fast pathway.
        slow_pathway = torch.index_select(
            frames,
            1,
            torch.linspace(
                0, frames.shape[1] - 1, frames.shape[1] // slowfast_alpha
            ).long(),
        )
        frame_list = [slow_pathway, fast_pathway]
        return frame_list

transform =  ApplyTransformToKey(
    key="video",
    transform=Compose(
        [
            UniformTemporalSubsample(num_frames),
            Lambda(lambda x: x/255.0),
            NormalizeVideo(mean, std),
            ShortSideScale(
                size=side_size
            ),
            CenterCropVideo(crop_size),
            PackPathway()
        ]
    ),
)

# The duration of the input clip is also specific to the model.
clip_duration = (num_frames * sampling_rate)/frames_per_second
device = 'cpu'
class TemporalDetection:
  def __init__(self, video_path, output_dir):
    #Change this model path
    self.model_feature_extraction_slowfast = torch.load('Models/slowfast_1sec_extractore.h5')
    self.video_path = video_path
    #
    self.MLP_Model = tf.keras.models.load_model('Models/best_model_standarized.h5')
    self.video = EncodedVideo.from_path( video_path )
    self.output_dir = output_dir
  def extract_features(self, ):
    num_of_clips= int(self.video.duration) // int(1.0666666666666667)
    print("Video clips: ", num_of_clips)
    print(self.video.duration)
    all_features = np.zeros((20, 2304))
    for clip_index, start_sec in enumerate(range(0, 20, int(clip_duration))):
          end_sec = min(start_sec + clip_duration, self.video.duration)

          # Load the desired clip (replace with your actual clip loading logic)
          video_data = self.video.get_clip(start_sec=start_sec, end_sec=end_sec)

          # Apply the transform
          video_data = transform(video_data)

          # Move the inputs to the desired device
          inputs = video_data["video"]
          inputs = [i.to(device)[None, ...] for i in inputs]

          with torch.no_grad():
              features = self.model_feature_extraction_slowfast(inputs)
          # Convert the features to a NumPy array
          features = features.cpu().numpy()
          features = features.reshape(features.shape[0], -1)
          if (start_sec <2):
                print(features.shape)
                all_features[clip_index] = features
    return all_features
  def make_predictions(self,):
    scaler = StandardScaler()
    features = self.extract_features()
    print(len(features))
    features = scaler.fit_transform(features)
    predictions = self.MLP_Model.predict(features)
    Binary_predictions = (predictions> 0.5).astype("int32")
    return Binary_predictions
  def concatenated_clips(self, labels):
    clips = []
    temp_clips = []
    for count, prediction in enumerate(labels):
      if prediction == 1 or prediction == 1.0:
        # print('entered')
        temp_clips.append(count)
      else:
        clips.append(temp_clips)
        temp_clips = []
    if prediction == 1:
      clips.append(temp_clips)
      temp_clips = []
    # print(temp_clips)
    clips = [sub_clip for sub_clip in clips if sub_clip]
    clips_by_one = clips
    tics_count =  sum(len(sub_array) for sub_array in clips)
    clips = [[sub_clip[0], sub_clip[-1]] for sub_clip in clips if sub_clip]
    return clips, tics_count, clips_by_one
  def save_video(self, video_tensor, output_path, fps=30):
      print(video_tensor)
      video_tensor = video_tensor.permute(1, 2, 3, 0)
      io.write_video(output_path, video_tensor, fps)
  def Temporal_Detection(self, ):

      preds = self.make_predictions()
      preds = np.array(preds).reshape(-1)
      clips_in_ranges, tics_count, clips = self.concatenated_clips(preds)
    #   print(clips)
    #   print(preds)
      output_files=[]
      for i, (start, end) in enumerate(clips_in_ranges):
          video_tensor = self.video.get_clip(start, end)
          print("******************start,end", start, end)
          output_file = os.path.join(self.output_dir, f'clip_{i+1}.mp4')
          self.save_video(video_tensor['video'], output_file)
          output_files.append(output_file)
      return {'clips_in_ranges': clips_in_ranges, "output_path": output_files, 'tics_count': tics_count, 'clips': clips, 'predictions': preds}

#To use this file in another project just import the file in the project and then make an object of the class TemporalDetection 
#and call the Temporal_Detection method


# detect_tics = TemporalDetection(
#     "downloaded_videos/subject1_video9.mp4", "upload_videos")
# temporals = detect_tics.Temporal_Detection()
# print(temporals)
