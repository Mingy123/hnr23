# Import TF and TF Hub libraries.
import tensorflow as tf
import cv2, time, csv, pickle, joblib
import numpy as np

vid = cv2.VideoCapture(0)
modelscorev2 = joblib.load('scoreregression.pkl' , mmap_mode ='r')
print(type(modelscorev2))

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

    result = modelscorev2.predict(np.array(row).reshape(1, -1))
    print(result)

