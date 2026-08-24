import cv2

from .loader import loadimage


def select_point(path):

    image = loadimage(path)
    display_image = image.copy()

    point = None
    window_name = "Select Object"

    def mouse_callback(event, x, y, flags, param):
        nonlocal point

        if event == cv2.EVENT_LBUTTONDOWN:

            point = (x, y)

            print(f"Selected point: {point}")

            display_image[:] = image

            cv2.circle(
                display_image,
                point,
                8,
                (0, 0, 255),
                -1
            )

            cv2.imshow(
                window_name,
                display_image
            )

    cv2.namedWindow(
        window_name,
        cv2.WINDOW_NORMAL
    )

    cv2.imshow(
        window_name,
        display_image
    )

    cv2.setMouseCallback(
        window_name,
        mouse_callback
    )

    print("Click on the object.")
    print("Press ENTER to confirm.")
    print("Press ESC to cancel.")

    while True:

        key = cv2.waitKey(20) & 0xFF

        if key == 13:  # ENTER

            if point is None:
                print("Please select a point first.")
                continue

            break

        elif key == 27:  # ESC
            point = None
            break

    cv2.destroyWindow(window_name)

    return point
