import cv2
import select 
import sys

def loadimage(path):
    image = cv2.imread(path)

    if image is None:
        raise FileNotFoundError(f"Could not load image: {path}")

    return image


def load_video(path):
    cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video: {path}")

    # frame per second
    fps = cap.get(cv2.CAP_PROP_FPS)

    def frames():
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            if select.select([sys.stdin], [], [], 0)[0]:
                key = sys.stdin.readline().strip()

                if key == "q":
                    break
                
            yield frame

        cap.release()

    return  frames(), fps

def load_video_by_camera(camera_index=0):
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        raise RuntimeError(
            f"Could not open camera with index: {camera_index}"
        )

    fps = cap.get(cv2.CAP_PROP_FPS)

    def frames():
        try:
            while True:
                ret, frame = cap.read()

                if not ret:
                    break

                yield frame

                # Check if something was typed in terminal
                if select.select([sys.stdin], [], [], 0)[0]:
                    key = sys.stdin.readline().strip()

                    if key == "q":
                        break

        finally:
            cap.release()

    return frames(), fps


if __name__ == "__main__":
	VIDEO_PATH = "examples/video.mp4"
	load_video(VIDEO_PATH)

