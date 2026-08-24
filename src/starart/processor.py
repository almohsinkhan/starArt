import cv2
import numpy as np

from .loader import loadimage

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

sam_processor = None
sam_model = None

def load_sam2():
	try:
		import torch
		from transformers import Sam2Processor, Sam2Model
	except ImportError:
		raise RuntimeError(
			"Silhouette mode required the SAM2 dependecies.\n"
			"Install then with: \n"
			"	pip install 'starart[sam2]'"
		)

	device = "cuda" if torch.cuda.is_available() else "cpu"

	global sam_processor
	global sam_model

	if sam_processor is None or sam_model is None:
		print("Loading SAM2...")

		sam_processor = Sam2Processor.from_pretrained(MODEL_ID)

		sam_model =Sam2Model.from_pretrained(MODEL_ID).to(device)

		sam_model.eval()
		print("SAM2 loaded.")

	return sam_processor, sam_model


def segment_image(path, x, y):

	sam_processor, sam_model = load_sam2()

	img = loadimage(path)

	# convert BGR -> RGB
	image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

	input_points = [[[[x, y]]]]
	input_labels = [[[1]]]

	inputs = sam_processor(
		images = image,
		input_points=input_points,
		input_labels=input_labels,
		return_tensors="pt").to(device)

	with torch.no_grad():
		outputs = sam_model(**inputs)

	# return multiple mask candiates
	masks = sam_processor.post_process_masks(
		outputs.pred_masks.cpu(),
		inputs["original_sizes"])[0]

	# First image, first cadidate mask
	mask = masks[0][0]

	# convert boolean mask to uint8
	mask = mask.numpy().astype("uint8")*255

	return mask


def ascii_art(path):
	image = loadimage(path)

	# Convert BGR image to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	return gray

def convert_to_ascii(image, chars):
    result = []

    for row in image:
        line = ""

        for pixel in row:
            index = int(pixel / 255 * (len(chars) - 1))
            line += chars[index]

        result.append(line)

    return result


if __name__ == "__main__":
	PATH = "../example/dog.jpg"
	print(ascii_art(PATH))
	# print("Final point:", point)
