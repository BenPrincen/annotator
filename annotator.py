import cv2
import os
from typing import List, Tuple

# How rendering should work for ImageLabeler
# - Have a render function that takes the bounding boxes for a specific image, and each time render gets called
# draw all the bounding boxes on the image.
# - Now show the image
# Image labeler should have a dictionary of lists that contain the bounding boxes for each image where the image path is the hash


class ImageLabeler:
    def __init__(self, image_dir):
        self.image_dir = image_dir
        self.image_files = [
            f
            for f in os.listdir(image_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
        ]
        self.current_index = 0
        self.current_image = self.load_image()
        self.bounding_boxes_per_img = {img_fname: [] for img_fname in self.image_files}
        self.drawing = False
        self.named_window = "Image Labeler"
        cv2.namedWindow(self.named_window)
        cv2.setMouseCallback(self.named_window, self.mouse_callback)

        self.load_image()

    def render(self) -> None:
        color = (0, 255, 12)
        display_img = self.current_image.copy()
        current_img_fname = self.image_files[self.current_index]
        bounding_boxes = self.bounding_boxes_per_img[current_img_fname]
        for bbox in bounding_boxes:
            pt1, pt2 = bbox
            cv2.rectangle(display_img, pt1, pt2, color, 2)
        cv2.imshow(self.named_window, display_img)

    def load_image(self) -> None:
        image_path = os.path.join(self.image_dir, self.image_files[self.current_index])
        self.current_image = cv2.imread(image_path)

    def get_current_bbox_list(self) -> List[List[Tuple[int]]]:
        current_img_fname = self.image_files[self.current_index]
        return self.bounding_boxes_per_img[current_img_fname]

    def mouse_callback(self, event, x, y, flags, param):
        current_img_fname = self.image_files[self.current_index]
        bounding_boxes = self.bounding_boxes_per_img[current_img_fname]
        if event == cv2.EVENT_LBUTTONDOWN:
            bounding_boxes.append([None, None])
            bounding_boxes[-1][0] = (x, y)
            bounding_boxes[-1][1] = (x, y)
            self.drawing = True
        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            bounding_boxes[-1][1] = (x, y)
            self.render()
        elif event == cv2.EVENT_LBUTTONUP:
            bounding_boxes[-1][1] = (x, y)
            self.render()
            self.drawing = False

    def run(self):
        while True:
            # call render here?
            self.render()

            key = cv2.waitKey(1) & 0xFF

            if key == ord("a"):
                self.current_index = (self.current_index - 1) % len(self.image_files)
                self.load_image()
            elif key == ord("d"):
                self.current_index = (self.current_index + 1) % len(self.image_files)
                self.load_image()
            elif key == 27:  # ESC key
                break
        # if self.current_image is not None:
        #     self.display_image = self.current_image.copy()
        # while True:
        #     if self.drawing:
        #         self.display_image1 = self.display_image.copy()
        #         if self.pt1 and self.pt2:
        #             cv2.rectangle(
        #                 self.display_image, self.pt1, self.pt2, (0, 255, 0), 2
        #             )
        #         cv2.imshow("Image Labeler", self.display_image)

        #     key = cv2.waitKey(1) & 0xFF

        #     if key == ord("a"):
        #         self.current_index = (self.current_index - 1) % len(self.image_files)
        #         self.load_image()
        #     elif key == ord("d"):
        #         self.current_index = (self.current_index + 1) % len(self.image_files)
        #         self.load_image()
        #     elif key == 27:  # ESC key to exit
        #         break


if __name__ == "__main__":
    image_dir = "..\\test_data\\yolo_dataset\\test\images"  # Replace with the path to your image directory
    labeler = ImageLabeler(image_dir)
    labeler.run()
    cv2.destroyAllWindows()
