import numpy as np
import socket
import cv2
from datetime import datetime
import time
import pyttsx3
t0=time.time()
time_list=[]

def timestamp():
    dt=datetime.now()
    dt=dt.strftime("%Y-%m-%d-%H-%M-%S")
    return dt

#mac address of samsung galaxy s5 being used as webcam 84:55:A5:DD:23:9C


if socket.gethostbyname(socket.gethostname())=='192.168.1.3':
    video=cv2.VideoCapture('http://192.168.1.93:8080/video')
else:
    video = cv2.VideoCapture('http://71.72.176.246:8080/video')

fps=24

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
frame_width = int(video.get(3))
frame_height = int(video.get(4))

video_output = cv2.VideoWriter(f'output_{timestamp()}.avi', fourcc, fps, (frame_width, frame_height))

ret, first_frame=video.read()
ret, second_frame=video.read()

text=''

while(video.isOpened()):
    status=0

    first_gray_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
    first_gray_frame = cv2.GaussianBlur(first_gray_frame, (5, 5), 0)

    second_gray_frame = cv2.cvtColor(second_frame, cv2.COLOR_BGR2GRAY)
    second_gray_frame = cv2.GaussianBlur(second_gray_frame, (5, 5), 0)

    delta_frame = cv2.absdiff(first_gray_frame, second_gray_frame)

    _, thresh_frame = cv2.threshold(delta_frame, 20, 255, cv2.THRESH_BINARY)
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=3)

    contours, _ = cv2.findContours(thresh_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        (x, y, w, h)=cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 1000:
            continue
        status=1
        cv2.rectangle(first_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        text='Motion Detected'
        cv2.putText(first_frame, text, (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 3)

    if text=='Motion Detected':
        video_output.write(first_frame)
        t0=time.time()
        time_list.append(t0)
        if t0 - time_list[0] > 10:
            break
        else:
            continue

    cv2.imshow('myframe', first_frame)
    first_frame=second_frame
    ret, second_frame=video.read()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release everything if job is finished
video.release()
video_output.release()
cv2.destroyAllWindows()
