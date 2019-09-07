# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 15:54:33 2019

@author: Xzw

E-mail: diligencexu@gmail.com
"""

import numpy as np
import pandas as pd

# 误差
def rssError(yArr,yHatArr): 
    return ((yArr-yHatArr)**2).sum()

# 标准化
def regularize(xMat):
    inMat = xMat.copy()
    inMeans = np.mean(inMat, 0)
    inVar = np.var(inMat, 0)
    inMat = (inMat - inMeans) / inVar
    return inMat

# 向前逐步回归
def stageWise(xArr, yArr, eps=0.01, numIt=100):
    xMat = np.mat(xArr)
    yMat = np.mat(yArr).T
    yMean = np.mean(yMat, 0)
    yMat = yMat - yMean
    xMat = regularize(xMat)
    m, n = np.shape(xMat)
    ws = np.zeros((n, 1))
    wsTest = ws.copy()
    wsMax = ws.copy()
    wsRec = ws.copy()
    for i in range(numIt):
        lowestError = np.inf; 
        for j in range(n):
            for sign in [-1, 1]:
                wsTest = ws.copy()
                wsTest[j] += eps * sign
                yTest = xMat * wsTest
                rssE = rssError(yMat.A, yTest.A)
                if rssE < lowestError:
                    lowestError = rssE
                    wsMax = wsTest
        ws = wsMax.copy()
        wsRec = np.concatenate((wsRec, ws), axis=1)
    return ws, pd.DataFrame(wsRec.T)