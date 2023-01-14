from flask import Flask
from threading import Thread
from datetime import datetime
import time, mingy, cv2

app = Flask(__name__)
mingy_ans = 0
PAUSE = 0.1
start_time = datetime.now()
frames = []
last_frame = None

@app.route("/jump")
def server():
    return str(mingy_ans)

def run_mingy():
    global mingy_ans
    while True:
        time.sleep(1)
        mingy_ans = mingy.main()

def background():
    global start_time
    global frames
    global last_frame
    # Copied from internet, must be correct
    # https://github.com/tensorflow/tensorflow/tree/master/tensorflow/lite/examples/python/
    interpreter = tf.lite.Interpreter(model_path="model.tflite")
    interpreter.allocate_tensors()

    while True:
        time.sleep(pause)
        ret, frame = cap.read()
        frame = cv2.resize(frame, (192, 192))

        # magic
        input_image = tf.cast(image, dtype=tf.float32)
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        interpreter.set_tensor(input_details[0]['index'], input_image.numpy())
        interpreter.invoke()

        # [1, 1, 17, 3] numpy array
        last_frame = interpreter.get_tensor(output_details[0]['index'])
        if len(frames) == 4: frames.pop(0)
        frames.append(last_frame)

def lock_sddm():
    print("---------")
    print("lock sddm")
    print("---------")

if __name__ == "__main__":
    # setting up the webcam
    cap = cv2.VideoCapture(0)
    a
    # mingy
    print('a')
    thread = Thread(target=run_mingy)
    print('running')
    thread.start()
    print('b')
    app.run(port=5000)
