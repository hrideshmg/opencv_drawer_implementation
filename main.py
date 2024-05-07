import os

import cv2
from PIL import Image, ImageDraw

centroids = []
for file in sorted(os.listdir("assets")):
    if file.endswith("png"):
        image = cv2.imread(f"assets/{file}")

        # Convert to grayscale as openCV doesnt like colour
        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Set any non-white pixels to full black
        _, threshold = cv2.threshold(grayscale, 200, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(
            threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        # Calculate center of pixel contour, contours[0] represents the edges of the image
        moment = cv2.moments(contours[1])
        center_x = moment["m10"] / moment["m00"]
        center_y = moment["m01"] / moment["m00"]

        # Find colour at the center point
        rgb_colour = tuple(image[int(center_y), int(center_x)])
        centroids.append(((center_x, center_y), rgb_colour))

canvas = Image.new("RGB", (256, 256), (256, 256, 256))
drawer = ImageDraw.Draw(canvas)
for point_index in range(0, len(centroids), 2):
    colour = centroids[point_index][1]
    drawer.line(
        (centroids[point_index][0], centroids[point_index + 1][0]),
        fill=colour,
        width=10,
    )
canvas.show()
