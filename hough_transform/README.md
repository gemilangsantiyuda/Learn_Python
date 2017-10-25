Using circular hough transform (CHT) and probabilistic line hough transform to detect lines and balls on grassfield.

In edge detection, i wrote my own implementation of kernel convolution over image. And surely it results in very slow convolution. It has to be redone in any way, maybe other way to convolve image, or optimization in the arithmatic operations using FFT (?).

I tried to code the CHT and probabilistic line HT but turned out to be super slow, so that I turn to scikit skimage library, and they are super fast. I have to learn the implementation!

To do the detection :
1. Low pass filter using 5x5 averaging kernel
2. High pass filter (edge detection) using sobel operator both Gx and Gy, and also the reversed sign sobel operator for Gx and Gy.
3. erasing edges on image border produced by the high pass filter.
3. Use the library to detect the circular object and the line.

results stored in result folder, and as can be seen the results are not reliable enough yet. It still miss eliptical line and still false detecting some area nearby image border as lines. image 7 shows the way I use the hough hough transform still giving terrible result in both detecting circular object and ignoring line-like noises.

Anyway this is for me a good beginning step to learn image processing! :D 
