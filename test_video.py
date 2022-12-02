"""Use this file to test if you can connect to your camera."""

import cv2


def testCamera(cam_cfg):

    cam_id = cam_cfg["index"]
    cam_api = cv2.CAP_ANY if cam_cfg["api"] == "any" else cv2.CAP_V4L2
    video_capture = cv2.VideoCapture(cam_id, cam_api)

    if not video_capture.isOpened():
        raise Exception("Could not open video device")

    # Set properties. Each returns === True on success (i.e. correct resolution)
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    while True:
        _, frame = video_capture.read()
        cv2.imshow("Stream", frame)

        if cv2.waitKey(1) == 27:
            break
