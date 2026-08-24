import cv2

image = cv2.imread("example/dog.jpg")

if image is None:
	print("Image Not loaded")
	exit()

cv2.namedWindow("Test", cv2.WINDOW_NORMAL)
cv2.imshow("Test", image)

print("window should be open now")
print("Press any key inside the window to close")

cv2.waitKey(0)
cv2.destroyAllWindows()
