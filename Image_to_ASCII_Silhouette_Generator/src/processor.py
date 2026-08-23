import cv2
import numpy as np

from .loader import loadimage

import torch
from transformers import Sam2Processor, Sam2Model


# resize the image
# define function for resize
def resize_image(image, terminal_width, terminal_height):
	h, w = image.shape[:2]
	height = int((h / w) * terminal_width * 0.5)

	if height > terminal_height:
		height = terminal_height

		terminal_width = int((w / h) * height / 0.5)

	return cv2.resize(image, (terminal_width, height),
			 interpolation=cv2.INTER_AREA)


def cleanMask(mask):
	kernel = np.ones((3, 3), np.uint8)
	mask = cv2.morphologyEx( mask, cv2.MORPH_OPEN, kernel)

	mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

	return mask

def processImage(path):
	img = loadimage(path)

	# call resize image function
	#re_image = resize_image(img)

	# convert the RGB image to gray scale
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# blur the image to remove the noise 
	blur = cv2.GaussianBlur(gray, (5, 5), 0)

	return gray

def thresholding(path):
	# process image
	img =  processImage(path)

	# thresholding
	threshold_value, mask = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

	return mask


def detect_edges(path, terminal_width, terminal_height):
	# Process image
	image = loadimage(path)

	image = resize_image(
		image,
		terminal_width,
		terminal_height
	)

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# canny algorithm to detect edge
	# upper threshold -> 200 , lower -> 100
	edges = cv2.Canny(gray, 100, 200)

	return edges

# model
MODEL_ID = "facebook/sam2.1-hiera-tiny"

device = "cuda" if torch.cuda.is_available() else "cpu"

processor = Sam2Processor.from_pretrained(MODEL_ID)

model = Sam2Model.from_pretrained(MODEL_ID).to(device)
model.eval()



def segment_image(path, x, y):
	img = loadimage(path)

	# convert BGR -> RGB
	image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

	input_points = [[[[x, y]]]]
	input_labels = [[[1]]]

	inputs = processor(
		images = image,
		input_points=input_points,
		input_labels=input_labels,
		return_tensors="pt").to(device)

	with torch.no_grad():
		outputs = model(**inputs)

	# return multiple mask candiates
	masks = processor.post_process_masks(
		outputs.pred_masks.cpu(),
		inputs["original_sizes"])[0]

	# First image, first cadidate mask
	mask = masks[0][0]

	# convert boolean mask to uint8
	mask = mask.numpy().astype("uint8")*255

	return mask



if __name__ == "__main__":
	IMAGE_PATH  =  "../example/dog.jpg"

	mask =  detect_edges(IMAGE_PATH)

	# take look at image
	cv2.imshow("grey image", mask)

	# 1. Keeps the window open until you press any key
	cv2.waitKey(0)

	# 2. Clears the window from your screen and frees up memory
	cv2.destroyAllWindows()
