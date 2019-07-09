import numpy as np
import unittest
import matplotlib.pyplot as plt
import warnings

'''
generate reportNum*perClientReport index data
'''
def change(oneValue, stringNum, sigma):
    while oneValue < 0 or oneValue >= stringNum:
        oneValue = np.random.normal(stringNum / 2, sigma)
    return int(oneValue)

class GenerateData():
    def __init__(self):
        self.filename = './clientRandomData.txt'
        self.clientNum = 100000
        self.perClientReport = 7
        self.reportNum = self.clientNum * self.perClientReport
        self.stringNum = 50
        self.sigma = self.stringNum / 10
        self.randomData = np.random.normal(self.stringNum / 2, self.sigma, self.reportNum)
        self.randomData = np.array([change(oneValue, self.stringNum, self.sigma) for oneValue in self.randomData])

    def drawData(self):
        # print(self.randomData)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        count, bins, ignored = ax.hist(self.randomData, int(self.stringNum), density=True)
        ax.set_title("Laplace ")
        # plt.xlim(-500, 500)
        # plt.legend()
        plt.show()

    def saveRandomData(self):
        arrayRandomData = self.randomData.reshape((self.clientNum, self.perClientReport))
        np.savetxt(self.filename, arrayRandomData, fmt='%d', delimiter='\t')
        print('save successfully!')

if __name__ == "__main__":

    gData = GenerateData()
    gData.drawData()
    gData.saveRandomData()