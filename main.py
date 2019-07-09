import numpy as np
import bitarray
import logging
from pybloom.pybloom import BloomFilter
from sklearn import linear_model
from collections import Counter
import matplotlib.pyplot as plt


# TODO load data and times
def loadData(filename):
    '''
    :return: clientData: (list clientNUm * perClientNUM)
    len(clientData): clientNUM
    len(clientData[0]): perClientReport
    stringUnique: string index
    resultList: statistic each string's number
    '''
    print('---loadData---')
    file = open(filename)
    clientData = []
    temp = {}
    result = {}
    for line in file.readlines():
        cutline = line.strip().split('\t')
        cutline = [int(x) for x in cutline]
        clientData.append(cutline)
        for x in cutline:
            if x not in temp:
                temp[x] = 1
            else:
                temp[x] += 1
    stringUnique = np.unique(clientData)
    for i in sorted(temp):
        result[i] = temp[i]
    resultList = [n for n in (result[i] for i in result)]
    return clientData, len(clientData), len(clientData[0]), stringUnique, resultList


# TODO init boolmfilter
def initBloomFilter(stringUnique):
    '''
    keyHashMat is (hahsLenth * keyNum)
    :param stringUnique:
    :return:
    '''
    print('---initialize Bloom Filter---')
    BF = BloomFilter(capacity=int(len(stringUnique) * 1.2), error_rate=0.30)
    keyHashMat = []
    for i in stringUnique:
        BF.add(i)
        keyHashMat.append([int(x) for x in BF.keyhash(i)])
    keyHashMat = np.mat(keyHashMat).T
    return BF, BF.num_bits, BF.bitarray, keyHashMat


# TODO deal with client data B
def data2B(clientData, BF):
    '''
    :return: Bdata(reportsNUM * k), sum num bitarray(1*k)
    '''
    print('\n---data -> B---')
    Bdata = []
    sumArray = np.array([0] * BF.num_bits)
    count = 0
    sumCount = len(clientData)
    for perClient in clientData:
        count += 1
        if count == int(sumCount * 0.25) \
                or count == int(sumCount * 0.5) \
                or count == int(sumCount * 0.75) \
                or count == int(sumCount):
            print(str(round(count / sumCount * 100, 2)) + ' %')
        for num in perClient:
            keyBitarray = BF.keyhash(num)
            keyArray = [int(x) for x in keyBitarray]
            sumArray += np.array(keyArray)
            Bdata.append(keyArray)
    return Bdata, sumArray


# TODO lasso regression
def lassoRegression(X, Y):
    '''
    :param X: hashLen*keyKindNUM
    :param Y: hashLen*1
    :return:  eachKeyNUM
    '''
    reg = linear_model.Lasso(alpha=0.1, positive=True)
    reg.fit(keyHashMat, sumMat)
    return reg.coef_


def compareResult(trueNUM, predictNUM):
    stringNum = len(trueNUM)
    x = np.arange(stringNum)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(x, trueNUM, width=0.4, facecolor='#9999ff', edgecolor='white', label='True')
    ax.bar(x + 0.4, predictNUM, width=0.4, facecolor='#ff9999', edgecolor='white', label='predict')
    # ax.bar(x, trueNUM, width=0.4, facecolor='#9999ff', edgecolor='white', label='True')
    # ax.bar(x + 0.4, predictNUM, width=0.4, facecolor='#ff9999', edgecolor='white', label='predict')
    ax.set_title("compare ")
    for a, b in zip(x, trueNUM):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)
    for a, b in zip(x, predictNUM):
        plt.text(a + 0.4, b + 800, '%.1f' % b, ha='center', va='bottom', fontsize=7)
    # plt.xlim(-500, 500)
    plt.legend()
    plt.show()


# TODO b2b'
def B2Bprime(Bdata, f):
    '''
    :param Bdata: (reportNum * hashLen)
    :return:
    '''
    print('\n---B -> B\'---')
    reportNum = len(Bdata)
    hashLen = len(Bdata[0])
    BprimeData = []
    count = 0
    for i in range(reportNum):
        count += 1
        if count == int(reportNum * 0.25) \
                or count == int(reportNum * 0.5) \
                or count == int(reportNum * 0.75) \
                or count == int(reportNum):
            print(str(round(count / reportNum * 100, 2)) + ' %')
        newOneReport = []
        for k in range(hashLen):
            randomNum = np.random.rand()
            if randomNum <= 0.5 * f:
                eachBit = 1
            elif randomNum <= f:
                eachBit = 0
            else:
                eachBit = Bdata[i][k]
            newOneReport.append(eachBit)
        BprimeData.append(newOneReport)
    return BprimeData


# TODO b'2s
def Bprime2S(BprimeData, p, q):
    '''
    :param BprimeData: (reportNum * hashLen)
    :return:
    '''
    print('---B\' -> S---\n')
    reportNum = len(BprimeData)
    hashLen = len(BprimeData[0])
    Sdata = []
    count = 0
    for i in range(reportNum):
        count += 1
        if count == int(reportNum * 0.25) \
                or count == int(reportNum * 0.5) \
                or count == int(reportNum * 0.75) \
                or count == int(reportNum):
            print(str(round(count / reportNum * 100, 2)) + ' %')
        newOneReport = []
        for k in range(hashLen):
            randomNum = np.random.rand()
            if BprimeData[i][k] == 1:
                if randomNum <= q:
                    eachBit = 1
                else:
                    eachBit = 0
            if BprimeData[i][k] == 0:
                if randomNum <= p:
                    eachBit = 1
                else:
                    eachBit = 0
            newOneReport.append(eachBit)
        Sdata.append(newOneReport)
    return Sdata


# TODO sDatg -> Y
def getPredictSumMat(Sdata, f, p, q):
    SdataMat = np.mat(Sdata)
    SumArray = np.array(np.sum(SdataMat, 0))[0]
    predictSumArray = [(x - (0.5 * f * q + p - 0.5 * f * p) * len(Sdata)) / ((1 - f) * (q - p)) for x in SumArray]
    return predictSumArray


if __name__ == '__main__':
    filename = './clientRandomData.txt'
    f = 0.5
    p = 0.5
    q = 0.75
    clientData, clientNum, perClientNum, stringUnique, resultList = loadData(filename)
    BF, BFnum_bits, BFbitarray, keyHashMat = initBloomFilter(stringUnique)
    Bdata, sumArray = data2B(clientData, BF)
    BprimeData = B2Bprime(Bdata, f)
    Sdata = Bprime2S(BprimeData, p, q)
    predictSumArray = getPredictSumMat(Sdata, f, p, q)
    sumMat = np.mat(predictSumArray).T
    predictNUM = lassoRegression(keyHashMat, predictSumArray)
    compareResult(resultList, predictNUM)

    # print(keyHashMat.I @ sumMat)
    # print('true num: ')
    # print(resultList)
    # print(keyHashMat @ np.mat(resultList).T)

    # sumMat = np.mat(sumArray).T
    # predictNUM = lassoRegression(keyHashMat, sumMat)
    # compareResult(resultList, predictNUM)
