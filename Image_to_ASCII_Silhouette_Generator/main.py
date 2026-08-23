from pathlib import Path
from src.renderer import renderer

import argparse

def main():
	parser = argparse.ArgumentParser(
		description="Convert images into ASCII StarArt."
	)

	# Image Path
	parser.add_argument(
		"image",
		type=Path,
		help="Path to the input image"
	)

	# Processing method
	parser.add_argument(
		"-m",
		"--mode",
		choices=["threshold", "outline", "silhouette"],
		default="outline",
		help="Image Processing mode (default: outline)"
	)

	# Output width
	parser.add_argument(
		"-w",
		"--width",
		type=int,
		help="Maximum output width"
	)

	# Character
	parser.add_argument(
		"-c",
		"--char",
		default="*",
		help="Character used to render the image"
	)

	args =  parser.parse_args()

	# check image exists
	if not args.image.exists():
		parser.error(
			f"Not a file: {args.image}"
		)

	if not args.image.is_file():
		parser.error(
			f"Not a file: {args.image}"
		)


	# validate width
	if args.width is not None and args.width <= 0:
		parser.error(
			f"Width much be greater than 0."
		)

	# Validate character
	if len(args.char) != 1:
		parser.error(
			"character much contain exactly one character."
		)

	renderer(args.image, args.mode, args.width, args.char)


if __name__ == "__main__":
    main()

