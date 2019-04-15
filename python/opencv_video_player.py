# encoding=utf-8
import sys
import numpy as np
import cv2

current_frame = None
current_frame_pos = -1


def trackbar_change(x):
    global current_frame, current_frame_pos
    current_frame_pos = x
    cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame_pos)
    ret, frame = cap.read()
    if ret:
        current_frame = frame
        cv2.imshow(winname, current_frame)


if __name__ == "__main__":

    if not len(sys.argv) == 2:
        print("Usage python [script-name] [video-path]")
        quit()

    print("Press q to quit!")

    video_name = sys.argv[1]
    cap = cv2.VideoCapture(video_name)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    print('frame_count =', frame_count)

    trackbar_name = 'frame_pos'
    winname = 'frame'

    cv2.namedWindow(winname)

    cv2.createTrackbar(trackbar_name, winname, 0,
                       int(frame_count), trackbar_change)

    cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame_pos)
    ret, current_frame = cap.read()

    while True:
        cv2.imshow(winname, current_frame)
        if cv2.waitKey(20) & 0xff == ord('q'):
            break

    cv2.destroyAllWindows()
