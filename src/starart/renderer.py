from turtle import width

from .processor import (thresholding, 
                        detect_edges, 
                        segment_image, 
						convert_to_ascii)

from .loader import loadimage, load_video
from .point_selector import select_point
from pathlib import Path
import cv2
import time 


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

def resize_ascii_image_for_terminal(image, width = None):
	terminal = shutil.get_terminal_size()

	if width is None:
		width = terminal.columns - 2
	else:
		width = min(width, terminal.columns - 2)


	h, w = image.shape[:2]

	height = int((h/ w) * width * 0.5)

	# leave some space for terminal 
	if height > terminal.lines - 2:
		height = terminal.lines - 2
		width = int((w/h) * height / 0.5)

	# resize the mask
	image = cv2.resize(
		image,
		(width, height),
		interpolation=cv2.INTER_AREA)

	return image

def renderer(path, mode, width=None, char="*"):
	
	if mode in ("ascii", "video") and char is None:
		char = " .:-=+*#%@"
	elif char is None:
		char = "*"
	
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

		point = select_point(path)

		if point is None:
			print("No point selected.")
			return
		x, y = point

		mask = segment_image(path, x, y)

	elif mode =="ascii":
		image = loadimage(path)

		# convert to gray scale

		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		image_height, image_width = image.shape

		# keep the characters roughlu square
		new_width = min(image_width, width)
		new_height = int(image_height * (new_width / image_width) * 0.5)

		image = resize_ascii_image_for_terminal(image, width)

		ascii_image = convert_to_ascii(image, char)

		for line in ascii_image:
			print(line)

		return 
	
	elif mode == "video":
		frames, fps = load_video(path)

		frame_time = 1 / fps

		first_frame = True

		for frame in frames:
			start_time = time.perf_counter()

			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			frame = resize_ascii_image_for_terminal(frame, width)

			ascii_image = convert_to_ascii(frame, char)

			if not first_frame:
				print(f"\033[{len(ascii_image)}A", end="")

			print("\n".join(ascii_image))

			elapsed_time = time.perf_counter() - start_time	
			remaining_time = frame_time - elapsed_time

			if remaining_time > 0:
				time.sleep(remaining_time)

			first_frame = False
			
		return 

	else:
		print("Invalid input")
		return


	if mode not in ("outline", "ascii", "video"):
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
