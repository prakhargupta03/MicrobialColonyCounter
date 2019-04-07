import numpy as np
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage as ndi
import imutils 
import cv2
import os
image_name = input('Input: ')
image_name = 'images/'+image_name
# image_name = 'images/'+'microbe1.1.png'
# image_name = '1.jpeg'
color_image =  cv2.imread( image_name, 1)
frame=  cv2.imread(image_name , 0)

frame = cv2.resize(frame,(600,600))
color_image = cv2.resize(color_image,(600,600))

kernel_size = 3
unique_colony = 0
while(unique_colony<10):
	# kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(9,9))
	kernel = np.ones((kernel_size,kernel_size),dtype= frame.dtype)

	# Step 1 Top Hat Transform
	tophat = cv2.morphologyEx(frame, cv2.MORPH_TOPHAT, kernel)

	# Step 2 OTSU's Threshold
	ret2,mask = cv2.threshold(tophat,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	# cv2.imshow("Output", mask)
	# cv2.waitKey(0)

	# """

	stencil = np.zeros(mask.shape).astype(mask.dtype)
	contours, hierarchy = cv2.findContours(mask.copy(),cv2.RETR_TREE ,cv2.CHAIN_APPROX_NONE)
	# print("Found %d objects." % len(contours))

	polyfillcontour = []
	# pointcontour = []
	for (i,c) in enumerate(contours):
		area = cv2.contourArea(c)
		flag = False
		if area<100000:
			if hierarchy[0,i,3] != -1:
				# print(len(c),area)
				flag = True
				# pointcontour.append(c)
				# cv2.drawContours(frame, c, -1, (255,0,0), 2)
				# cv2.drawContours(im2, c, -1, (127), 2)
		if not flag:
			polyfillcontour.append(c)
			# cv2.drawContours(maskedImage,[c],-1,127,2)

	cv2.fillPoly(stencil, polyfillcontour, [255,255,255])
	stencil = cv2.bitwise_not(stencil)
	result = cv2.bitwise_and(mask, stencil)
	# cv2.drawContours(result, pointcontour, -1, (127), 2)

	# mask = cv2.bitwise_and(mask, maskedImage, mask=maskedImage)

	distance = ndi.distance_transform_edt(result)
	local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((3, 3)),
								labels=result)
	markers = ndi.label(local_maxi)[0]
	labels = watershed(-distance, markers, mask=result)
	unique_colony = len(np.unique(labels)) - 1
	# print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))
		
	# loop over the unique labels returned by the Watershed algorithm
	for label in np.unique(labels):
		# if the label is zero, we are examining the 'background'
		# so simply ignore it
		if label == 0:
			continue
	 
		# otherwise, allocate memory for the label region and draw
		# it on the mask
		mask1 = np.zeros(mask.shape, dtype="uint8")
		mask1[labels == label] = 255
	 
		# detect contours in the mask and grab the largest one
		cnts = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		c = max(cnts, key=cv2.contourArea)
	 
		# draw a circle enclosing the object
		((x, y), r) = cv2.minEnclosingCircle(c)
		cv2.circle(color_image, (int(x), int(y)), int(r), (0,205, 0), 2)
	 
	# show the output image
	kernel_size=kernel_size+2
	# """
cv2.imwrite('images/output.png',color_image)
delay = 1000000000000
while delay>0:
	delay = delay-1
	
# import base64

# with open("output.png", "rb") as image_file:
	# encoded_string = base64.b64encode(image_file.read())
	# print(encoded_string)

print(unique_colony)

# os.remove(image_name)

## config