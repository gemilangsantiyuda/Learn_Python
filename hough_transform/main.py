from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import cm
import array
import tugas
import numpy as np
from skimage import data, color, measure
from skimage.transform import hough_circle, hough_circle_peaks, probabilistic_hough_line
from skimage.draw import circle_perimeter
from skimage.util import img_as_ubyte
from skimage.transform import (hough_line, hough_line_peaks,probabilistic_hough_line)
import math

"""The selection of kernel for use!"""
averageX = 1/25.00000000000
averageKernel = [[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]
gaussianX = 1/273.000000000
gaussianKernel = [[1,4,7,4,1],[4,16,26,16,4],[7,26,41,26,7],[4,16,26,16,4],[1,4,7,4,1]]
sobelGx1 = [[1,0,-1],[2,0,-2],[1,0,-1]]
sobelGy1 = [[1,2,1],[0,0,0],[-1,-2,-1]]
sobelGx2 = [[-1,0,1],[-2,0,2],[-1,0,1]]
sobelGy2 = [[-1,-2,-1],[0,0,0],[1,2,1]]
sobelDg = [[2,1,0],[1,0,-1],[0,-1,-2]]
robertGx = [[1,0],[0,-1]]
robertGy = [[0,1],[-1,0]]
"""The selection of kernel for use!"""


fileName = r"images/8.jpg"

im = Image.open(fileName)

#still playing on grayscale image, converting to grayscale and numpy array of it!
imL = im.convert("L")
imDarrayL = np.array(imL)

#low pass filter
imL  = tugas.ConvolveImage(averageKernel,imL,averageX)

#highpass filter
imX1 = tugas.ConvolveImage(sobelGx1,imL,1.5)
imY1 = tugas.ConvolveImage(sobelGy1,imL,1.5)
imX2 = tugas.ConvolveImage(sobelGx2,imL,1.5)
imY2 = tugas.ConvolveImage(sobelGy2,imL,1.5)
#combining them using absolut addition and high threshold of 255
imNew = tugas.CombineDensity(tugas.CombineDensity(imX1,imY1),tugas.CombineDensity(imX2,imY2))

#again low pass filter to blur the edge noise
imNew = tugas.ConvolveImage(averageKernel,imNew,averageX)
imNew.show()

imDarray = np.array(imNew)

#thresholding with low threshold of 100
#because the input of the library method of CHT and PLHT is numpy array of 1 and 0
# pixel with intensity > 100 will have the value 1 in numpy array, else it has 0
h = len(imDarray)
w = len(imDarray[1])
for i in range(h):
  for j in range(w):
    if i in range(3) or j in range(3) or i in range(h-3,h) or j in range(w-3,w):
      imDarray[i][j]=1
    if imDarray[i][j]>100 :
      imDarray[i][j] = 1
    else :
      imDarray[i][j] = 0


#CHT
hough_radii = np.arange(50, 200, 2)
hough_res = hough_circle(imDarray, hough_radii)
accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                           total_num_peaks=1)

fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(10, 4))
image = np.array(im)

for center_y, center_x, radius in zip(cy, cx, radii):
    circy, circx = circle_perimeter(center_y, center_x, radius)
    for a in range(h):
      for b in range(w):  
        ya = center_y-a
        ya*=ya
        xb = center_x-b
        xb*=xb       
        if abs(math.sqrt(ya+xb))<=radius+4:
          imDarray[a][b]=0
    plt.text(center_x,center_y,str(center_y)+","+str(center_x), bbox=dict(facecolor='red', alpha=0.5))
    image[circy, circx] = (220, 20, 20)
#plotting the ball outline 
ax.imshow(image, cmap=plt.cm.gray)

#PLHT
lines = probabilistic_hough_line(imDarray, threshold=10,line_length=80,line_gap=3)
#plotting the lines
for line in lines:
  p0, p1 = line
  ax.plot((p0[0], p1[0]), (p0[1], p1[1]),'-r')
plt.show()
