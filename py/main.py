from flask import Flask, Response
from threading import Thread
from datetime import datetime
import tensorflow as tf
import time, mingy, walnit, cv2

app = Flask(__name__)
mingy_buf = []
walnit_ans = "placeholder"
walnit_count = 0
walnit_buf = []
PAUSE = 0.1
TIMEOUT = 3600
start_time = datetime.now()
four_hour_count = 0
frames = []
last_frame = None
cap = cv2.VideoCapture(0)
walnit_activate = False
nobody_count = 0
JUMP_ACCEPT = 30


@app.route('/log/<action>', methods=['POST'])
def logged_in(action):
    global walnit_activate
    if action == 'in':
        walnit_activate = True
    elif action == "out":
        walnit_activate = False
    else:
        return action + " is not a valid option. Use 'in' or 'out'"
    return "Done"

@app.route('/jumping')
def jumping():
    global mingy_buf
    count = 0
    for i in mingy_buf:
        if i == "proper":
            count += 1
    print(count, len(mingy_buf))
    if count > JUMP_ACCEPT:
        mingy_buf = []
        return '2'
    elif count > JUMP_ACCEPT / 2:
        return '1'
    return '0'


@app.route('/cameraon')
def cameraon():
    global cap
    try:
        cap.release()
    except:
        pass
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


# Copied from internet, must be correct
# https://github.com/tensorflow/tensorflow/tree/master/tensorflow/lite/examples/python/
def magic():
    _, frame = cap.read()
    frame = cv2.resize(frame, (192, 192))
    image = tf.convert_to_tensor(frame)
    image = tf.expand_dims(image, axis=0)
    interpreter = tf.lite.Interpreter(model_path="model.tflite")
    interpreter.allocate_tensors()
    input_image = tf.cast(image, dtype=tf.float32)
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.set_tensor(input_details[0]['index'], input_image.numpy())
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    keypoints = output.reshape(-1, 3)
    return keypoints


def background():
    global frames, last_frame, mingy_buf, walnit_ans, walnit_count, walnit_buf, nobody_count
    while True:
        time.sleep(PAUSE)
        now = datetime.now()
        if (now - start_time).seconds > TIMEOUT:
            lock_sddm()
        last_frame = magic()
        left = last_frame[5]
        right = last_frame[6]
        dist = (left[0]-right[0])**2 + (left[1]-right[1])**2
        if dist ** 0.5 < 25/192:
            nobody_count += 1
            if nobody_count > 20:
                print("nobody")
                nobody_count = 0
                mingy_buf = []
                continue
        else: nobody_count = 0

        if len(frames) == 5: frames.pop(0)
        frames.append(last_frame)

        ### mingy
        ans = mingy.main(frames)
        if len(mingy_buf) == 40: mingy_buf.pop(0)
        mingy_buf.append(ans)

        # Walnit checks time hehe
        if not walnit_activate:
            continue
        walnit_count += 1 # Make sure runs at 1fps
        if walnit_count == 10:
            if len(walnit_buf) > 3: walnit_buf.pop()
            walnit_buf.insert(0, last_frame)
            walnit.main(walnit_buf) # Run analysis code
            walnit_count = 0


def lock_sddm():
    four_hour_count += 1
    if four_hour_count == 8:
        os.system("shutdown now")
    os.system("loginctl lock-session")


if __name__ == "__main__":
    thread = Thread(target=background)
    thread.start()
    app.run(port=5000)

'''
ret, frame = cap.read()
frame = cv2.resize(frame, (192, 192))

# magic
input_image = tf.cast(frame, dtype=tf.float32)
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
interpreter.set_tensor(input_details[0]['index'], input_image.numpy())
interpreter.invoke()

# [1, 1, 17, 3] numpy array
last_frame = interpreter.get_tensor(output_details[0]['index'])
'''
