from .processor import thresholding, detect_edges, resize_image, segment_image
from pathlib import Path
import cv2


def renderer(path, method):

	# select method
	if method == 1:
		mask = thresholding(path)
	elif method == 2:
		mask = detect_edges(path)
	elif method == 3:
		mask = resize_image(segment_image(path, 300, 200))
	else:
		print("Invalid input")
		return 


	for row in mask:
		for pixel in row:
			if pixel == 255:
				print("*", end="")
			else:
				print(" ", end="")
		print()

if __name__ == "__main__":
	dir_path = Path("../example")
	files = [p.name for p in dir_path.iterdir()]

	# print them with there index
	i = 1
	for file in files:
		print(f"{i}.{file}")
		i+=1

	# user input for test
	test_file = int(input("image to test (index): "))

	IMAGE_PATH = dir_path / files[test_file-1]

	# list of methods
	method = int(input("\n1.Thresholding (filled object) \n2.Canny (outline) \n3.Segment method(filled object) \n select method : "))

	print(f"testing  {IMAGE_PATH} Using {method} ", end="\n")

	renderer(IMAGE_PATH, method)

"""
cv2.imshow("Mask", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
