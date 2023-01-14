'''
NOTE
this code will open the webcam and save data into jump_dataset
'''


# Import TF and TF Hub libraries.
import tensorflow as tf
import cv2, time, csv

vid = cv2.VideoCapture(0)
f = open("jump_dataset.csv", "a")
writer = csv.writer(f)

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
    for point in range(5,13):
        row.append(keypoints[point][0])
        row.append(keypoints[point][1])
    row.append("sitting")
    writer.writerow(row)
    EDGES = { (5, 7), (7, 9), (6, 8), (8, 10), (5, 6), (5, 11), (6, 12), (11, 12) }

    for i, (start, end) in enumerate(EDGES):
        start_point = (int(keypoints[start][1] * 192), int(keypoints[start][0] * 192))
        end_point = (int(keypoints[end][1] * 192), int(keypoints[end][0] * 192))
        cv2.line(frame, start_point, end_point, (255, 0, 0), 2)

    # Display the input image with the skeleton overlay
    cv2.imshow("Skeleton", frame)
    key = cv2.waitKey(100)
    if key == ord('q'):
        cv2.destroyAllWindows()
        break

f.close()
