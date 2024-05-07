import os
import re

import cv2
from PIL import Image, ImageDraw

centroids = []

# Sort files numerically
files = sorted(os.listdir("assets"), key=lambda x: float(re.findall("(\d+)", x)[0]))

for file in files:
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
        if len(contours) == 1:
            centroids.append("break")
            continue

        moment = cv2.moments(contours[1])
        center_x = moment["m10"] / moment["m00"]
        center_y = moment["m01"] / moment["m00"]

        # Find colour at the center point
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        rgb_colour = tuple(rgb_image[int(center_y), int(center_x)])

        centroids.append(((center_x, center_y), rgb_colour))

# Draw a black canvas
canvas = Image.new("RGB", (512, 512), (256, 256, 256))
drawer = ImageDraw.Draw(canvas)

# Only start drawing from every 2nd point in the list
for point_index in range(0, len(centroids) - 1):
    if centroids[point_index + 1] == "break" or centroids[point_index] == "break":
        print(point_index + 1)
        continue

    colour = centroids[point_index][1]
    drawer.line(
        (centroids[point_index][0], centroids[point_index + 1][0]),
        fill=colour,
        width=20,
    )

canvas.show()
