from PIL import Image
import matplotlib.pyplot as plt
import array
import tugas
x = 1/9.00000000000
averageKernel = [[1,1,1],[1,1,1],[1,1,1]]
fileName = r"images/2.jpg"
nCluster = 2

im = Image.open(fileName)
im = im.convert("L")
im.show()

im = tugas.ConvolveImage(averageKernel,im,x)
im.show()
histogram = tugas.MakeHistogram(im)
plt.plot(histogram)
#plt.show()

imClustered = tugas.HistogramCluster(im,nCluster)
imClustered.show()
