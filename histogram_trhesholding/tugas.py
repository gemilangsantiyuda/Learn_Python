from PIL import Image
import array
import math
import copy
#BEGIN HISTOGRAM CLUSTER
def HistogramCluster(inputImage,numCluster):
  colors = [0,255,128]
  histogram = MakeHistogram(inputImage)
  cluster = []
  bins = []
  mean = 0
  freq = 0
  stdDeviation = 0
  for i in range(256):
    mean+=(histogram[i]*i)
    freq+=histogram[i]
  mean/=freq
  for i in range(256):
    stdDeviation += (histogram[i]*pow((i-mean),2))
  stdDeviation/=(freq-1)
  stdDeviation = math.sqrt(stdDeviation)
  #print(mean," ",stdDeviation)
  
  #K-Means initialization of cluster center by taking the most densest bins 
  #initializing bins width using Terrell (1990) bin width estimation rule  
  binWidth = math.ceil(1.144*stdDeviation/pow(freq,1/5))
  #print(binWidth)
  start = 0
  end = binWidth
  while start< 255 :
    freqBin = 0
    meanBin = 0
    for i in range(start,end+1):
      meanBin+=histogram[i]*i
      freqBin+=histogram[i]
    if freqBin!=0 :
      meanBin/=freqBin
    bins.append([meanBin,freqBin])
    #print(meanBin," ")
    start = end+1
    end = min(255,end+binWidth)
  #print(bins,"\n")
  for i in range(numCluster):
    bestMean = -1
    bestFreq = -1
    for j in range(len(bins)):
      if bins[j][1]>bestFreq:
        bestFreq = bins[j][1]
        bestMean = bins[j][0]
    cluster.append(int(bestMean))
    for j in range(len(bins)):
      bins[j][1] = (bins[j][1]*(1-math.exp(-numCluster*pow(bestMean-bins[j][0],2))))
      #print(math.exp(-numCluster*pow(bestMean-bins[j][0],2))," ")
    #print(bins,"\n")
  #print(cluster)
  cluster = sorted(cluster)
  found = True
  while found :
    newCluster = []
    start = 0
    for i in range(numCluster):
      end = 0
      if i == numCluster-1:
        end = 255
      else :
        end = int((cluster[i] + cluster[i+1])/2)
      newPoint = 0
      freq = 0
      for j in range(start,end+1):
        newPoint+=(histogram[j]*j)
        freq+=histogram[j]
      newPoint/=freq
      newCluster.append(int(newPoint) )
    found = not (newCluster == cluster)
    cluster = copy.deepcopy(newCluster)
    #print(newCluster," ",newCluster == cluster)
  clusterMember = []
  start = 0
  for i in range(len(cluster)):
    if i == numCluster-1:
      end = 255
    else :
      end = int((cluster[i] + cluster[i+1])/2)
    clusterMember.append([])
    for j in range(start,end+1):
      clusterMember[i].append(j)
    start = end+1
  imList = list(inputImage.tobytes())
  for i in range(len(imList)) :
    for j in range(len(clusterMember)):
      if imList[i] in clusterMember[j]:
        imList[i]=colors[j]
        break
  print(cluster)
  imNew = Image.frombytes("L",inputImage.size,array.array('B',imList).tostring())
  return imNew
#END

#BEGIN MAKE HISTOGRAM FREQUENCY LIST
def MakeHistogram(inputImage):
  imList = list(inputImage.tobytes())
  histogram = []
  for i in range(256):
    histogram.append(0)

  for i in imList:
    histogram[i]+=1
  return histogram
#END


#BEGIN CONVOLUTION
def ConvolveImage(kernel,inputImage,constanta = 1.000):
	#Change the picture into 2Dlist of bytes
	width,height = inputImage.size
	imList = list(inputImage.tobytes())
	imListNew = []
	temp = []
	j = 0

	for i in range(len(imList)):
		j = (j+1)%width
		temp.append(imList[i])
		if(j==0):
			imListNew.append(temp)
			temp=[]
			j=0
	imList = imListNew[:]
	imListNew = []
	kernelNew = []			
	#flip horizontal vertical of kernel
	ii = -1
	for i in reversed(range(len(kernel))):
		kernelNew.append([])
		ii+=1
		for j in reversed(range(len(kernel[0]))):
			kernelNew[ii].append(kernel[i][j])
	kernel = kernelNew[:]
	#Convolve the kernel onto the image 
	ks = int(len(kernel)/2)#kernelStep
	for i in range(height):
		for j in range(width):
			newDen = 0
			for y in range(len(kernel)):
				if(i+y-ks<0 or i+y-ks>=height):
					continue
				for x in range(len(kernel)):
					if(j+x-ks<0 or j+x-ks>=width):
						continue
					newDen+=(kernel[y][x]*imList[i+y-ks][j+x-ks])
			#print(newDen)	
			imListNew.append(int(float(newDen)*constanta))

	#Convert the lists back into image
	imList = []
	for i in imListNew:
		j = i
		#thresholding <0 to 0 , >255 to 255
		if(j>255):
			j=255
		imList.append(j)
		#print(j)
	#print(len(imList))
	imNew = Image.frombytes("L",(width,height),array.array('B',imList).tostring())
	return imNew

#END OF convolveImage 

#BEGIN combineDensity
def CombineDensity(im1,im2):
	imNew1 = list(im1.tobytes())
	imNew2 = list(im2.tobytes())
	imNew3 = []
	for i in range(len(imNew1)):
		imNew3.append(imNew1[i]+imNew2[i])
		if(imNew3[i]>255):
			imNew3[i]=255
	imNew3 = Image.frombytes("L",(im1.size),array.array("B",imNew3).tostring())
	return imNew3
#END OF combineDensity	
