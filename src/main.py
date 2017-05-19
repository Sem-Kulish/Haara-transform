import cv2
import numpy as np


def grayColor(image):
    p = image.shape
    for i in range(p[0]):
        for j in range(p[1]):
            intensityOfPixel = image[i, j][0] * 0.11 + image[i, j][1] * 0.53 + image[i, j][2] * 0.36
            image[i, j] = [intensityOfPixel, intensityOfPixel, intensityOfPixel]

def scaleToMaxIntens(val):
    return 127.5+val*127.5

def scaleToZeroOne(val):
    return (-127.5+val)/127.5


def FWT(data, w0, w1, s0, s1):
    temp = np.zeros(data.shape[0])

    h = data.shape[0] >> 1

    for i in range(h):
        k = i << 1
        temp[i] = data[k]*s0+data[k+1]*s1
        temp[i+h] = data[k]*w0+data[k+1]*w1

    for j in range(data.shape[0]):
        data[j]=temp[j]

def IWT(data, w0, w1, s0, s1):
    temp = np.zeros(data.shape[0])

    h = data.shape[0] >> 1

    for i in range(h):
        k = i << 1
        temp[k] = (data[i]*s0+data[i+h]*w0)/w0
        temp[k+1] = (data[i]*s1+data[i+h]*w1)/s0

    for j in range(data.shape[0]):
        data[j] = temp[j]


def FWTA(data, w0, w1, s0, s1, iterations):
    length = data.shape[0]
    num = data.shape[1]

   # row = np.zeros(cols)
    #col = np.zeros(rows)

    for i in range(iterations):

        num1 = 1 << (i & 31)
        num2 = num/num1
        num3 = length/num1
        numArray = np.zeros(int(num2))

        for j in range(int(num3)):
            for k in range(numArray.shape[0]):
                numArray[k] = data[j, k]

            FWT(numArray, w0, w1, s0, s1)

            for k in range(numArray.shape[0]):
                data[j, k] = numArray[k]

        numArray1 = np.zeros(int(num3))
        for k in range(int(num2)):
            for j in range(numArray1.shape[0]):
                numArray1[j] = data[j, k]

            FWT(numArray1, w0, w1, s0, s1)

            for j in range(numArray1.shape[0]):
                data[j, k] = numArray1[j]

def IWTA(data, w0, w1, s0, s1, iterations):
    length = data.shape[0]
    num = data.shape[1]

    #row = np.zeros(rows)
    #col = np.zeros(cols)

    for i in range(iterations-1, 0-1, -1):

        num1 = 1 << (i & 31)
        num2 = num/num1
        num3 = length/num1
        numArray = np.zeros(int(num3))

        for j in range(int(num2)):
            for k in range(numArray.shape[0]):
                numArray[k] = data[k, j]

            IWT(numArray, w0, w1, s0, s1)

            for k in range(numArray.shape[0]):
                data[k, j] = numArray[k]

        numArray1 = np.zeros(int(num2))
        for k in range(int(num3)):
            for j in range(numArray1.shape[0]):
                numArray1[j] = data[k, j]

            IWT(numArray1, w0, w1, s0, s1)

            for j in range(numArray1.shape[0]):
                data[k, j] = numArray1[j]


image = cv2.imread('../images/lena.png')

cv2.imshow('Original image', image)

koef = 8

w0 = 0.5
w1 = -0.5
s0 = 0.5
s1 = 0.5

procImage = image.copy()

red = np.zeros((procImage.shape[0],procImage.shape[1]))
green = np.zeros((procImage.shape[0],procImage.shape[1]))
blue = np.zeros((procImage.shape[0],procImage.shape[1]))

#grayColor(procImage)

for i in range(procImage.shape[0]):
    for j in range(procImage.shape[0]):
        red[i, j] = scaleToZeroOne(procImage[i, j][0])
        green[i, j] = scaleToZeroOne(procImage[i, j][1])
        blue[i, j] = scaleToZeroOne(procImage[i, j][2])


FWTA(red, w0, w1, s0, s1, koef)
FWTA(green, w0, w1, s0, s1, koef)
FWTA(blue, w0, w1, s0, s1, koef)

for i in range(procImage.shape[0]):
    for j in range(procImage.shape[1]):
        procImage[i, j][0] = scaleToMaxIntens(red[i, j])
        procImage[i, j][1] = scaleToMaxIntens(green[i, j])
        procImage[i, j][2] = scaleToMaxIntens(blue[i, j])

cv2.imshow("Processed image", procImage)

red = np.zeros((procImage.shape[0],procImage.shape[1]))
green = np.zeros((procImage.shape[0],procImage.shape[1]))
blue = np.zeros((procImage.shape[0],procImage.shape[1]))

for i in range(procImage.shape[0]):
    for j in range(procImage.shape[0]):
        red[i, j] = scaleToZeroOne(procImage[i, j][0])
        green[i, j] = scaleToZeroOne(procImage[i, j][1])
        blue[i, j] = scaleToZeroOne(procImage[i, j][2])

IWTA(red, w0, w1, s0, s1, koef)
IWTA(green, w0, w1, s0, s1, koef)
IWTA(blue, w0, w1, s0, s1, koef)

resImage = procImage.copy()

for i in range(resImage.shape[0]):
    for j in range(resImage.shape[1]):
        resImage[i, j][0] = scaleToMaxIntens(red[i, j])
        resImage[i, j][1] = scaleToMaxIntens(green[i, j])
        resImage[i, j][2] = scaleToMaxIntens(blue[i, j])

cv2.imshow("Restored image", resImage)

cv2.waitKey(0)
cv2.destroyAllWindows()