from flask import Flask
from threading import Thread
import time, mingy

app = Flask(__name__)
mingy_ans = 0

@app.route("/")
def server():
    return str(mingy_ans)

def run_mingy():
    global mingy_ans
    while True:
        time.sleep(1)
        mingy_ans = mingy.main()

if __name__ == "__main__":
    # mingy
    print('a')
    thread = Thread(target=run_mingy)
    print('running')
    thread.start()
    print('b')
    app.run(port=5000)
