import cv2
import pytesseract
from threading import Thread
import time
import serial
#ser = serial.Serial('COM3', 9600,timeout = 0.05)
camera01 = []
camera02 = []


# MUST HAVE LINE
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def camera1():
    global camera01
    LastNumber = None
    ListNumber1 = []
    video1 = cv2.VideoCapture(0)

# Allows continuous frames

    while (True):
        # Capture each frame from the video feed
        ret, frames = video1.read()
        if ret == True and len(camera01)==0:

            try:
                data4 = pytesseract.image_to_data(frames)
            except:
                continue
            for z, a in enumerate(data4.splitlines()):
                # Counter
                if z != 0:
                    # Converts 'data1' string into a list stored in 'a'
                    # print(len(a))
                    a = a.split()
                    # Checking if array contains a word
                    if len(a) == 12:
                        # Storing values
                        m, n = int(a[6]), int(a[7])
                        p, q = int(a[8]), int(a[9])
                        # Display bounding box of each word
                        cv2.rectangle(frames, (m, n),
                                      (m + p, n + q), (0, 255,0), 2)
                        # Display detected word under each bounding box
                        cv2.putText(frames, a[11], (m - 15, n),
                                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1)
                        if a[11].isdigit():
                            if (a[11] != LastNumber):
                                LastNumber = a[11]
                                ListNumber1.append(LastNumber)

                            break

            cv2.imshow("Camera 1", frames)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            video1.release()
            cv2.destroyAllWindows()
            break
        if ListNumber1 != [] and len(camera01) == 0:
            camera01 = ListNumber1
            ListNumber1 = []

def camera2():
    global camera02
    video2 = cv2.VideoCapture(1)
    FirstNumber = None
    ListNumber2 = []
    while True:

        ret1, frame = video2.read()
        if ret1 == True and len(camera02)==0:
            try:
                data5 = pytesseract.image_to_data(frame)
            except:
                continue
            for number, b in enumerate(data5.splitlines()):
                if number != 0:
                    b = b.split()
                    if len(b) == 12:
                        xid, yid = int(b[6]), int(b[7])
                        wid, hid = int(b[8]), int(b[9])
                        cv2.rectangle(frame, (xid, yid),
                                      (xid + wid, yid + hid), (0, 255, 0), 2)
                        cv2.putText(frame, b[11], (xid - 15, yid),
                                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 1)
                        if b[11].isdigit():
                            if (b[11] != FirstNumber):
                                FirstNumber = b[11]
                                ListNumber2.append(FirstNumber)
                            break

            cv2.imshow("Camera 2", frame)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            video2.release()
            cv2.destroyAllWindows()
            break
        if ListNumber2 != [] and len(camera02) == 0:
            camera02 = ListNumber2
            ListNumber2 = []

th = Thread(target=camera1)
th.start()
th1 = Thread(target=camera2)
th1.start()

while True:
    # for i in range(len(camera01)):
    #     for j in range(len(camera02)):
    #         if i == j:
    #             if camera01[i] == camera02[j]:
    #                 print('checked')
    #             else:
    #                 print('wrong')
    #         else:
    #             continue
    # camera01 = []
    # camera02 = []
    if (len(camera01) == 1 and len(camera02) == 1):
        for i in range(len(camera01)):
            for j in range(len(camera02)):
                if i == j:
                    if camera01[i] == camera02[j]:
                        #ser.write(b'0')
                        print('checked')
                    else:
                        #ser.write(b'1')
                        print('wrong')
                else:
                    continue
        #time.sleep(5)
        camera01 = []
        camera02 = []