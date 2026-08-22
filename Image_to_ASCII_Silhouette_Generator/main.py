from pathlib import Path
from src.renderer import renderer


def main():

    dir_path = Path("example")

    files = [p.name for p in dir_path.iterdir()]

    i = 1

    for file in files:
        print(f"{i}. {file}")
        i += 1

    test_file = int(input("image to test (index): "))

    IMAGE_PATH = dir_path / files[test_file - 1]

    method = int(input(
        "\n"
        "1. Thresholding (filled object)\n"
        "2. Canny (outline)\n"
        "3. Segmentation (filled object)\n"
        "Select method: "
    ))

    print(f"Testing {IMAGE_PATH} using method {method}")

    renderer(IMAGE_PATH, method)


if __name__ == "__main__":
    main()
