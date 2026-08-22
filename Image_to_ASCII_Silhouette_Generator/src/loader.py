import cv2

def loadimage(path):
    image = cv2.imread(path)

    if image is None:
        raise FileNotFoundError(f"Could not load image: {path}")

    return image

if __name__ == "__main__":
	IMAGE_PATH = input("Image path : ")
	img  = loadimage(IMAGE_PATH)
	cv2.imshow("god image", img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
