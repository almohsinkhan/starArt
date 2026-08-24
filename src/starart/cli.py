from pathlib import Path
from .renderer import renderer

import argparse

def main():
	parser = argparse.ArgumentParser(
	description="Convert images into terminal-based ASCII StarArt.",
	epilog=(
		"Examples:\n"
		"  starart dog.jpg\n"
		"  starart dog.jpg --mode threshold\n"
		"  starart dog.jpg --mode outline --width 80\n"
		"  starart dog.jpg --mode silhouette\n"
		"  starart dog.jpg --mode outline --char \"#\"\n"
		"  starart dog.jpg --mode ascii\n"
		"  starart dog.jpg --mode ascii --width 80"
	),
	formatter_class=argparse.RawDescriptionHelpFormatter,
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
		choices=["threshold", "outline", "silhouette", "ascii"],
		default="outline",
		help=(
            "Image processing mode: "
            "threshold=filled object, "
            "outline=edge detection, "
            "silhouette=SAM2 segmentation, "
            "ascii=grayscale ASCII art "
            "(default: outline)"),
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
		default=None,
		help="Character used to render the image. For ascii mode, provide a brightness gradient."
	)

	args =  parser.parse_args()

	# check if image exist
	if not Path(args.image).is_file():
		parser.error(f"Image file not found: {args.image}")

	# validate width
	if args.width is not None:
		if args.width <= 0:
			parser.error(
				f"Width must be greater than 0."
			)
		if args.width > 300:
			parser.error(
				f"Width must not exceed 300."
			)


	# Validate character
	if args.char is not None:
		if args.mode == "ascii" and len(args.char) < 2:
			parser.error("ASCII character gradient must contain at least 2 characters.")
		elif args.mode != "ascii" and len(args.char) != 1:
			parser.error("Character must contain exactly one character.")

	try:
		renderer(args.image, args.mode, args.width, args.char)
	except RuntimeError as e:
		print(f"\nError: {e}")


if __name__ == "__main__":
    main()
