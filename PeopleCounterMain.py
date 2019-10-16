import argparse
import datetime
import imutils
import math
import cv2
import numpy as np


def testIntersectionIn(x, y):
    res = -450 * x + 400 * y + 157500
    if ((res >= -550) and (res < 550)):
        return True
    return False


def testIntersectionOut(x, y):
    res = -450 * x + 400 * y + 180000
    if ((res >= -550) and (res <= 550)):
        return True
    return False


def peopleCounter(capture, width=800):
    """peopleCounter function
    
    Arguments:
        capture {cv2.Capture} -- cv2 capture object which is
        requited to feed system with frames 
    
    Keyword Arguments:
        width {int} -- frame width (default: {800})
    """
    firstFrame = None
    textIn = 0
    textOut = 0
    # it is based on previous value
    # for width 800 it was set to 12000
    # for varible width I set it to 12000 = width^2 * k
    # k is calvulated as 0.01875
    contourAreaTreshold = (width**2) * 0.01875

    print('To exit please press q')
    # loop over the frames of the video
    while True:
        # grab the current frame and initialize the occupied/unoccupied
        # text
        (grabbed, frame) = capture.read()
        text = "Unoccupied"

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if not grabbed:
            break

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=width)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < contourAreaTreshold:
                continue
            # compute the bounding box for the contour, draw it on the frame,
            # and update the text
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.line(frame, (width // 2, 0), (width, 450), (250, 0, 1), 2)  # blue line
            cv2.line(frame, (width // 2 - 50, 0), (width - 50, 450), (0, 0, 255), 2)  # red line

            rectagleCenterPont = ((x + x + w) // 2, (y + y + h) // 2)
            cv2.circle(frame, rectagleCenterPont, 1, (0, 0, 255), 5)

            if (testIntersectionIn((x + x + w) // 2, (y + y + h) // 2)):
                textIn += 1

            if (testIntersectionOut((x + x + w) // 2, (y + y + h) // 2)):
                textOut += 1

            # draw the text and timestamp on the frame

            # show the frame and record if the user presses a key
            # cv2.imshow("Thresh", thresh)
            # cv2.imshow("Frame Delta", frameDelta)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        cv2.putText(frame, "In: {}".format(str(textIn)), (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, "Out: {}".format(str(textOut)), (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        cv2.imshow("Security Feed", frame)

    # cleanup the capture and close any open windows
    capture.release()
    cv2.destroyAllWindows()

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Count passing people from the selected video source')
    parser.add_argument(
        "source", 
        help="the directory of the image which will be opened"
        )
    parser.add_argument(
        "-w", "--width",
        help="video frame width of the video source",
        type=int
    )

    args = parser.parse_args()
    capture = cv2.VideoCapture(args.source)
    if args.width:
        peopleCounter(capture, width=args.width)
    else:
        peopleCounter(capture)


if __name__ == "__main__":
    main()