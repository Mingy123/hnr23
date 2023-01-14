from flask import Flask, Response
from threading import Thread
from datetime import datetime
import time, mingy, cv2

app = Flask(__name__)
mingy_buf = []
walnit_ans = None
PAUSE = 0.1
start_time = datetime.now()
frames = []
last_frame = None
cap = cv2.VideoCapture(0)

@app.route('/cameraon')
def cameraon():
    try: cap.release()
    except: pass
    cap = cv2.VideoCapture(0)
    return "Done"

# this may kill the video_feed
@app.route('/cameraoff')
def cameraoff():
    cap.release()
    return "Done"

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            ret, frame = cap.read()
            ret, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

def background():
    global frames, last_frame
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

        # actual calculations
        now = datetime.now()
        if (now - start_time).seconds > TIMEOUT:
            lock_sddm()
        ### mingy
        global mingy_buf
        ans = mingy.main(frames)
        if len(mingy_buf) == 10: mingy_buf.pop(0)
        mingy_buf.append(ans)
        ### walnit
        global walnit_ans
        walnit.warn() # TODO: this is not implemented yet

def lock_sddm():
    print("---------")
    print("lock sddm")
    print("---------")

if __name__ == "__main__":
    # mingy
    thread = Thread(target=run_mingy)
    thread.start()
    app.run(port=5000)
