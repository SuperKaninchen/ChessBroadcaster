import cv2
import sys


def checkCam(index, use_usb, use_v4l2):
    print(f"Checking camera with index {index}")
    print(f"Flags: use_usb={use_usb} use_v4l2={use_v4l2}")
    if not use_usb:
        # To use Tapo Cameras.
        broadcast_info = BroadcastInfo()
        pwd = broadcast_info.camera_password
        camera_ip = broadcast_info.IPs[4]
        RTSP_URL = f"rtsp://camera5:{pwd}@{camera_ip}/stream1"
        cap_index = RTSP_URL
        cap_api = cv2.CAP_FFMPEG
    else:
        # To use with an USB camera (or DroidCam).
        # You may need to change the index to other (small) integer values if you have multiple cameras.
        cap_index = index
        # You may need to try different cap_api's. The default is CAP_ANY. Use CAP_V4L2 in Linux.
        if not use_v4l2:
            cap_api = cv2.CAP_ANY
        else:
            cap_api = cv2.CAP_V4L2

    try:
        video_capture = cv2.VideoCapture(cap_index, cap_api)
        if not video_capture.isOpened():
            print("Failure!")
            return False
        else:
            if "--view" in sys.argv:
                print("Showing current camera, press ESC to close")
                video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                while True:
                    _, frame = video_capture.read()
                    cv2.imshow(f"Camera {index}", frame)

                    if cv2.waitKey(1) == 27:
                        cv2.destroyAllWindows()
                        break
            return True
    except Exception as e:
        return False


def checkIndex(index):
    out = []

    # Test using USB and CAP_ANY
    result = checkCam(i, True, False)
    out.append({"index": i,
                "use_usb": True,
                "use_v4l2": False,
                "result": result})
    if result:
        print("Success!")
        if not "--all" in sys.argv:
            return out

    # Test using USB and CAP_V4L2
    result = checkCam(i, True, True)
    out.append({"index": i,
                "use_usb": True,
                "use_v4l2": True,
                "result": result})
    if result:
        print("Success!")
        if not "--all" in sys.argv:
            return out

    return out


if __name__ == "__main__":
    if sys.argv[1] in ["-h", "--help"]:
        print("""Arguments:
    --view      show current camera stream
    --all       dont quit on success (check all indices)""")
    else:
        all_results = {}
        for i in range(6):
            all_results[i] = checkIndex(i)
            print(f"Done testing index {i}")
            if not "--all" in sys.argv:
                break
        for index in all_results.keys():
            print(f"\nResults for index {index}:")
            for result in all_results[index]:
                print("\t", end="")
                print("use_usb: " + str(result["use_usb"]), end=", ")
                print("use_v4l2: " + str(result["use_v4l2"]), end=", ")
                print("functional: " + str(result["result"]))
