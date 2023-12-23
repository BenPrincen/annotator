import cv2
import os
import numpy as np
from typing import List

# Global variables
top_left_pt = (-1, -1)
bottom_right_pt = (-1, -1)
img = None
img_copy = None


# Mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global top_left_pt, bottom_right_pt, img, img_copy

    drawing = False

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        top_left_pt = (x, y)
        img_copy = img.copy()

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        bottom_right_pt = (x, y)
        img_copy = img.copy()
        cv2.rectangle(img_copy, top_left_pt, bottom_right_pt, (0, 255, 0), 2)
        cv2.imshow("Image with Bounding Box", img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        bottom_right_pt = (x, y)
        img_copy = img.copy()
        cv2.rectangle(img_copy, top_left_pt, bottom_right_pt, (0, 255, 0), 2)
        cv2.imshow("Image with Bounding Box", img_copy)


# Function to load all images in a directory
# possibly load on demand in the future to reduce memory usage?
def load_images(folder_path: str) -> List[np.ndarray]:
    assert os.path.exists(folder_path), f"Path {folder_path} does not exist"
    assert os.path.isdir(folder_path), f"Path {folder_path} must be a directory"
    images = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith((".png", ".jpg", ".jpeg", ".gif")):
            img_path = os.path.join(folder_path, filename)
            img = cv2.imread(img_path)
            if img is not None:
                images.append((filename, img))
    return images


# Function to display images and handle key events
def display_images(images):
    global img, img_copy
    current_index = 0
    num_images = len(images)

    while True:
        _, image = images[current_index]
        img = image
        if img_copy:
            cv2.imshow("Image with Bounding Box", img_copy)
        else:
            cv2.imshow("Image with Bounding Box", img)
        key = cv2.waitKey(0)
        print(f"key: {key}")
        if key == 27:  # ESC key to exit
            break
        elif key == 97:  # A key
            current_index = (current_index - 1) % num_images
        elif key == 100:  # D key
            current_index = (current_index + 1) % num_images

    cv2.destroyAllWindows()


if __name__ == "__main__":
    folder_path = "..\\test_data\\yolo_dataset\\test\images"  # Change this to the path of your image folder
    image_list = load_images(folder_path)
    assert image_list, "No images found in the specified folder."
    cv2.namedWindow("Image with Bounding Box")
    cv2.setMouseCallback("Image with Bounding Box", draw_rectangle)
    display_images(image_list)
