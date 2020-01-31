# record a video and play it
import numpy as np
import cv2

filename = 'video.avi'

# SAVING
    # to save a video, 3 things are needed
    # output name, f. e.: 'video.avi'
    # FourCC code, which specify the video codec. The preffered for Windows id DIVX
    # FourCC is passed as cv2.VideoWriter_forcc('M', 'J', 'P', 'G') or
    # cv2.VideoWriter_fourcc(*'MJPG')
    # isColor flag - if True, encoder expects color frame, otherwise returns grayscale
    # size
    # frames


def record():
    cap = cv2.VideoCapture(0)

    four_cc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, four_cc, 20.0, (640, 480))

    while cap.isOpened():
        ret, frame = cap.read()
        # first returned value - ret - is a bool
        # and checks wheter the frame is read correctly

        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame = cv2.flip(frame, 1) # second parameter is a code, in which direction should th frame be flipped

        out.write(frame)

        # cv2.imshow('frame', gray)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    out.release()
    cap.release()



def play():
    cap = cv2.VideoCapture(filename)

    while cap.isOpened():
        ret, frame = cap.read()

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    


if __name__ == "__main__":
    play()

    cv2.destroyAllWindows()