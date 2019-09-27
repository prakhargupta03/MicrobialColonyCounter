# Importing libraries
import numpy as np
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage as ndi
import imutils 
import cv2
import os
# Importing libraries over

# Take image input. Image must be in same folder as code
image_name = input('Input: ')
image_name = 'images/'+image_name

## now read image from path user entered. 

# read image as color image. (See second arguement of imread function)
color_image =  cv2.imread( image_name, 1)
# read same image as grayscale image. (See second arguement of imread function)
frame=  cv2.imread(image_name , 0)

#  next line is to get height and width of image
m,n = frame.shape

# resize images to 600 pixel by 600 pixel
frame = cv2.resize(frame,(600,600))
color_image = cv2.resize(color_image,(600,600))

# Initial kernel size in 7. Kernel is just a matrix. Kernel is used for top hat transform
kernel_size = 7

# initially unique colonies were 0.
unique_colony = 0

# image_part2 is used to keep copy of original image for future operations in code
image_part2 = color_image
	
# repeat process until we have at least 10 colonies or kernel size is less than 18
while(unique_colony<10 and kernel_size<18):
	# create a matrix or kernel of size equal to kernel_size. All entries inside matrix are 1
	kernel = np.ones((kernel_size,kernel_size),dtype= frame.dtype)

	# Step 1 Top Hat Transform. 
	# morphologyEx function(first argument is image, second is to tell that we have to perform top hat transform operation, third argument is kernel)
	tophat = cv2.morphologyEx(frame, cv2.MORPH_TOPHAT, kernel)

	# Step 2 OTSU's Threshold
	# otsu will convert image to black and white
	# threshold function(first is image name we just applied top hat operation, second in min value of threshold, third is max value of threshold, last is which technique to follow of otsu )
	ret2,mask = cv2.threshold(tophat,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	
	# next two lines are optional. Use only if you want to see how image looks after otsu threshold
	# cv2.imshow("Output", mask)
	# cv2.waitKey(0)

	
	# Step 3. Detect outer circle.
	# once circle detected, take only portion inside circle and make circle make circle and portion outside circle black to that in image only content inside circle is left.
	
	
	stencil = np.zeros(mask.shape).astype(mask.dtype)
	
	# find outer circle
	contours, hierarchy = cv2.findContours(mask.copy(),cv2.RETR_TREE ,cv2.CHAIN_APPROX_NONE)

	# empty list. we will append all circles found in image inside this
	polyfillcontour = []
	
	# for each circle found inside in image do following.
	#(these circles can be outer contour or colony)
	for (i,c) in enumerate(contours):
		# for each circle,find area of such circle 
		area = cv2.contourArea(c)
		flag = False
		# if area is less than 100000 than is is not outer contour, so we need to ignore it
		if area<100000:
			# this is to detect if circle is present inside circle, if so than it cannot be outer circle i.e contour
			if hierarchy[0,i,3] != -1:
				flag = True
		# finally if is is contour, then add it to polyfillcontour list 
		if not flag:
			polyfillcontour.append(c)
			
	# next 3 lines remove outer circle and content after outer circle so than these are not counted while counting colonies
	cv2.fillPoly(stencil, polyfillcontour, [255,255,255])
	stencil = cv2.bitwise_not(stencil)
	result = cv2.bitwise_and(mask, stencil)

	# next lines are to apply watershed algorithm
	distance = ndi.distance_transform_edt(result)
	# print(distance)
	local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((3, 3)),
								labels=result)
	markers = ndi.label(local_maxi)[0]
	labels = watershed(-distance, markers, mask=result)
	unique_colony = len(np.unique(labels)) - 1
		
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
	 
		# draw a circle enclosing the object. this is green circle around detected colonies
		((x, y), r) = cv2.minEnclosingCircle(c)
		cv2.circle(color_image, (int(x), int(y)), int(r), (0,205, 0), 2)

	kernel_size=kernel_size+2
	
kk = unique_colony
	
## if colony detection failed due to now finding outer circle, then count without circle. 
## The following code is duplicate of above code with only detecting outer circle part removed

if(unique_colony<10):
	kernel_size = 17
	color_image = image_part2
	
	kernel = np.ones((kernel_size,kernel_size),dtype= frame.dtype)

	# Step 1 Top Hat Transform
	tophat = cv2.morphologyEx(frame, cv2.MORPH_TOPHAT, kernel)

	# Step 2 OTSU's Threshold
	ret2,mask = cv2.threshold(tophat,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	stencil = np.zeros(mask.shape).astype(mask.dtype)
	contours, hierarchy = cv2.findContours(mask.copy(),cv2.RETR_TREE ,cv2.CHAIN_APPROX_NONE)

	result = mask
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
	 
	
# write output	

# following code is to add output (i.e number of colonies) at the bottom of image.
color_image = cv2.resize(color_image,(n,m))

border=cv2.copyMakeBorder(color_image, top=0, bottom=25, left=0, right=0, borderType= cv2.BORDER_CONSTANT, value=[0,0,0])

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,m+15)
fontScale              = 0.5
fontColor              = (255,255,255)
lineType               = 1

# putText function write text on image
cv2.putText(border,str(unique_colony), 
    bottomLeftCornerOfText, 
    font, 
    fontScale,
    fontColor,
    lineType)
	
if(unique_colony<1000):
	cv2.putText(border," colonies detected", (40,m+15),font,0.4,fontColor,lineType)
else:
	cv2.putText(border," colonies detected", (48,m+15),font,0.4,fontColor,lineType)

if(kk<10):
	cv2.putText(border,"Contour not detected.", (n-130,m+15),font,0.3,fontColor,lineType)

cv2.imwrite('images/output.png',border)

delay = 10000
while delay>0:
	delay = delay-1
	
print(unique_colony)