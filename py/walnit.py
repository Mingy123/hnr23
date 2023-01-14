import joblib, os
from subprocess import Popen
import numpy as np

modelscorev2 = joblib.load('posture/scoreregression.pkl' , mmap_mode ='r')
process = None

def check(frames):
    past_few = []
    for keypoints in frames:
        row = []
        for point in range(9):
            row.append(keypoints[point][0])
            row.append(keypoints[point][1])

        # predict posture
        past_few.append(modelscorev2.predict(np.array(row).reshape(1, -1))[0])

    print("Walnit:", past_few)

    # indeed will defo not hire me over the code below
    flag = len(past_few) == 4
    for item in past_few:
        flag = past_few[0] == item and flag

    if flag:
        global process
        if past_few[0] != "proper" and process is None:
            if past_few[0] == "side" and os.path.exists("STOPCHECKLOOK"):
                pass
            else:
                print("triggering", past_few[0])
                process = Popen(['python', 'posture/tk_thread.py', past_few[0]])
        elif past_few[0] == "proper" and process is not None:
            print("Killing!")
            process.kill()
            process = None

