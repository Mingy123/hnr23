'''
NOTE
this code uses the pkl file and queries the ai with a frame captured by cv2
actually, i will save 4 frames in the buffer since that's how we trained the ai
'''


# Import TF and TF Hub libraries.
import tensorflow as tf
import cv2, csv, joblib
import numpy as np

modelscorev2 = joblib.load('workout/jumpmodel.pkl' , mmap_mode ='r')

def main(frames):
    if len(frames) != 5: return
    buffer = []
    for i in frames:
        for point in range(5, 13):
            buffer.append(i[point][0])
            buffer.append(i[point][1])
    result = modelscorev2.predict(np.array(buffer).reshape(1, -1))
    return result
