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
    rows = data.shape[0]
    cols = data.shape[1]

    row = np.zeros(cols)
    col = np.zeros(rows)

    for k in range(iterations):
        for i in range(rows):
            for j in range(row.shape[0]):
                row[j] = data[i, j]

            FWT(row, w0, w1, s0, s1)

            for j in range(row.shape[0]):
                data[i, j] = row[j]

        for j in range(cols):
            for i in range(col.shape[0]):
                col[i] = data[i, j]

            FWT(col, w0, w1, s0, s1)

            for i in range(col.shape[0]):
                data[i, j] = col[i]

def IWTA(data, w0, w1, s0, s1, iterations):
    rows = data.shape[0]
    cols = data.shape[1]

    row = np.zeros(rows)
    col = np.zeros(cols)

    for k in range(iterations):
        for j in range(rows):
            for i in range(row.shape[0]):
                col[i] = data[i, j]

            IWT(col, w0, w1, s0, s1)

            for i in range(row.shape[0]):
                data[i, j] = col[i]

        for i in range(cols):
            for j in range(col.shape[0]):
                row[j] = data[i, j]

            IWT(row, w0, w1, s0, s1)

            for j in range(col.shape[0]):
                data[i, j] = row[j]


image = cv2.imread('../images/lena.png')

cv2.imshow('Original image', image)

koef = 1

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
