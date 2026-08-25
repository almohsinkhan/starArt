import cv2

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

            yield frame

        cap.release()

    return  frames(), fps


if __name__ == "__main__":
	VIDEO_PATH = "examples/video.mp4"
	load_video(VIDEO_PATH)

