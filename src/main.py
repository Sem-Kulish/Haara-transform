import cv2
import numpy as np
import random as rn
import math

def grayColor(image):
    p = image.shape
    for i in range(p[0]):
        for j in range(p[1]):
            intensityOfPixel = image[i, j][0] * 0.11 + image[i, j][1] * 0.53 + image[i, j][2] * 0.36
            image[i, j] = [intensityOfPixel, intensityOfPixel, intensityOfPixel]

def calcParamMatrixCoefs(coefArray):
    for i in range(coefArray.shape[0]):
        coefArray[i, 0] = i

    n = 0
    p = 0
    q = 0
    for j in range(0, 10240):
        if 2**j == coefArray.shape[0]:
            n = j
    print(n)
    for k in range(coefArray.shape[0]):
        while k != 2**p + q - 1:
            p = rn.randrange(0, n)
           # print(p)
            q = 0
            if p == 0:
                q = 1
            elif p != 0:
                q = rn.randrange(1, 2**p+1)
                #print(q)
            #print(p, " <- p ", q, " <- q")
        coefArray[k, 1] = p
        coefArray[k, 2] = q
       # print(coefArray[k])
    return coefArray
def calcTransformMatrixElem(N, p, q, z):
    if (q - 1) / 2**p <= z < (q - 0.5) / 2**p:
        return 2**(p/2)/math.sqrt(N)*1
    elif (q - 0.5) / 2**p <= z < q / 2**p:
        return -1*2**(p/2)/math.sqrt(N)
    else:
        return 0

def TransformMatrix(coefArray, matrix):
    for i in range(matrix.shape[0]):
        p = coefArray[i, 1]
        q = coefArray[i, 2]
        for j in range(matrix.shape[0]):
            N = matrix.shape[0]
            z = j / N
            matrix[i, j]=calcTransformMatrixElem(N, p, q, z)

    return matrix

image = cv2.imread('../images/2.png')

if image.shape[0]!=image.shape[1]:
    print("Error! Wrong image!")
    exit(1)
cv2.imshow("Image", image)

#grayColor(image)



coefs = np.zeros((image.shape[0], 3))
H = np.zeros((image.shape[0], image.shape[0]))

calcParamMatrixCoefs(coefs)
H = TransformMatrix(coefs, H)

print(H)

HT = H.copy()
HT = np.transpose(HT)

F = np.zeros((image.shape[0], image.shape[1]))

for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        F[i, j] = image[i, j][0]



T = H*F*HT
print(T)

procimage = image.copy()

for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        procimage[i, j] = [T[i, j], T[i, j], T[i, j]]

cv2.imshow("Processed image", procimage)
#print(HT)

cv2.waitKey(0)
cv2.destroyAllWindows()