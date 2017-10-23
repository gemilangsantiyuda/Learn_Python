from PIL import Image
import matplotlib.pyplot as plt
import array
import tugas
averageX = 1/9.00000000000
averageKernel = [[1,1,1],[1,1,1],[1,1,1]]
gaussianX = 1/273.000000000
gaussianKernel = [[1,4,7,4,1],[4,16,26,16,4],[7,26,41,26,7],[4,16,26,16,4],[1,4,7,4,1]]
sobelGx = [[1,0,-1],[2,0,-2],[1,0,-1]]
sobelGy = [[1,2,1],[0,0,0],[-1,-2,-1]]
fileName = r"images/1.jpg"
nCluster = 2

im = Image.open(fileName)
imL = im.convert("L")
#im.show()

#im = tugas.ConvolveImage(averageKernel,im,x)
imL  = tugas.ConvolveImage(gaussianKernel,imL,gaussianX)
imX = tugas.ConvolveImage(sobelGx,imL,1.5,100,99)
imY = tugas.ConvolveImage(sobelGy,imL,1.5)
imNew = tugas.CombineDensity(imX,imY)
#imNew.show()

rect = tugas.DetectCircle(imNew)


