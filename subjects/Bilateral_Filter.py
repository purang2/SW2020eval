# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 13:21:15 2020

@author: 전자공학부 은찬
"""


import cv2
import numpy as np
import timeit

img =cv2.imread("VOLIBEAR.jpg")

#가우시안 필터적용 --1
blur1 = cv2.GaussianBlur(img, (5,5), 0)

#바이레터럴 필터적용 --2
    #src = 입력 이미지
    #d   = 필터 size(직경) // 5의 경우 ->5x5필터
    #sigmaColor = 클수록 이웃한 픽셀의 영향 커짐(색 공간 필터의 시그마값) 
    #sigmaSpace = 좌표 공간의 시그마 값(sigmaColor와 같은 값이 보통 권장됨)
st=timeit.default_timer()
blur2 = cv2.bilateralFilter(src=img,d=5,sigmaColor=50, sigmaSpace=50)
tm=timeit.default_timer()
print("Running time: %f" %(tm-st))

#결과 출력

merged = np.hstack((img,blur1,blur2))
cv2.imshow('bilateral',merged)
cv2.waitKey(0)
cv2.distoryAllWindows()


