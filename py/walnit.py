# Import TF and TF Hub libraries.
import tensorflow as tf
import cv2, csv, joblib
import numpy as np

modelscorev2 = joblib.load('scoreregression.pkl' , mmap_mode ='r')

def main(frame):
    keypoints = frame.reshape(-1, 3)
    row = []
    for point in range(9):
        row.append(keypoints[point][0])
        row.append(keypoints[point][1])
    result = modelscorev2.predict_proba(np.array(row).reshape(1, -1))
    return result[0]
