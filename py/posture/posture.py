import tensorflow as tf
import cv2, time, csv, pickle, joblib
import numpy as np
from subprocess import Popen

vid = cv2.VideoCapture(0)
modelscorev2 = joblib.load('scoreregression.pkl', mmap_mode='r')

past_few = []
process = None

while True:
    _, frame = vid.read()
    frame = cv2.resize(frame, (192, 192))
    image = tf.convert_to_tensor(frame)
    image = tf.expand_dims(image, axis=0)

    # Initialize the TFLite interpreter
    interpreter = tf.lite.Interpreter(model_path="../model.tflite")
    interpreter.allocate_tensors()

    # TF Lite format expects tensor type of float32.
    input_image = tf.cast(image, dtype=tf.float32)
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], input_image.numpy())

    interpreter.invoke()

    # Output is a [1, 1, 17, 3] numpy array.
    output = interpreter.get_tensor(output_details[0]['index'])
    keypoints = output.reshape(-1, 3)

    row = []
    for point in range(9):
        row.append(keypoints[point][0])
        row.append(keypoints[point][1])
    # load the model from disk

    result = modelscorev2.predict(np.array(row).reshape(1, -1))[0]
    if len(past_few) > 3: past_few.pop()
    past_few.insert(0, result)

    # indeed will defo not hire me over the code below
    flag = len(past_few) == 4
    for item in past_few:
        flag = past_few[0] == item and flag

    if flag:
        if past_few[0] != "proper" and process is None:
            print("triggering", past_few[0])
            process = Popen(['python', 'tk_thread.py', past_few[0]])
        elif past_few[0] == "proper" and process is not None:
            print("Killing!")
            process.kill()
            process = None


    print(past_few, flag)


    time.sleep(1)
