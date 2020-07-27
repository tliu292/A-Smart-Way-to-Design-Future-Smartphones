# import the necessary packages
import numpy as np
import glob
import cv2
import os
# os.environ['OPENCV_IO_ENABLE_JASPER'] = '1'
def auto_canny(image, sigma=0.5):
	# compute the median of the single channel pixel intensities
	v = np.median(image)
	# apply automatic Canny edge detection using the computed median
	lower = int(max(0, (1.0 - sigma) * v))
	upper = int(min(255, (1.0 + sigma) * v))
	edged = cv2.Canny(image, lower, upper)
	# return the edged image
	return edged

import ntpath
ntpath.basename("./")
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
# loop over the images
for imagePath in glob.glob("test.png"):
    image = cv2.imread(imagePath)
    print(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    tight = cv2.Canny(blurred, 160, 165)
    auto = auto_canny(blurred)
    import pathlib
    pathlib.Path('demo').mkdir(parents=True, exist_ok=True)
    filePath = "demo/" + path_leaf(imagePath)
    cv2.imwrite(filePath, auto) 
