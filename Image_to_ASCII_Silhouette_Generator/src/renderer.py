from .processor import thresholding, detect_edges, segment_image
from pathlib import Path
import cv2

# import for termial operation dealing
import shutil

# resize for termial
def resize_mask_for_terminal(mask, width = None):
	terminal = shutil.get_terminal_size()

	if width is None:
		width = terminal.columns - 2
	else:
		width = min(width, terminal.columns - 2)


	h, w = mask.shape[:2]

	height = int((h/ w) * width * 0.5)

	# leave some space for terminal 
	if height > terminal.lines - 2:
		height = terminal.lines - 2
		width = int((w/h) * height / 0.5)

	# resize the mask
	mask = cv2.resize(
		mask,
		(width, height),
		interpolation=cv2.INTER_NEAREST)

	return mask


def renderer(path, mode, width=None, char="*"):

	terminal = shutil.get_terminal_size()

	if width is None:
		width = terminal.columns - 2

	height = terminal.lines - 2

	# select method
	if mode == "threshold" :
		mask = thresholding(path)

	elif mode == "outline":
		mask = detect_edges(path, width, height)

	elif mode == "silhouette":
		mask = segment_image(path, width, height)

	else:
		print("Invalid input")
		return

	if mode != "outline":
		mask = resize_mask_for_terminal(mask, width)


	for row in mask:
		for pixel in row:
			if pixel == 255:
				print(char, end="")
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
