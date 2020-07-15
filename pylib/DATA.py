import os
import parDict
import numpy as np
from matplotlib import cm
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter


class DATA():
    k = 0
    args = None

    def __init__(self, CLs_map, grid, success, contour=None):
        self.CLs = CLs_map
        self.grid = grid
        self.success = np.array(success, dtype=bool)
        self.contour = contour
        self.axis = dict.fromkeys([0, 1])
        self.axisInd = {0: [None, None], 1: [None, None]}
        self.prepared = False

    def _prepare(self):
        for i in range(2):
            self.makeAxis(i)
        self.prepareData()
        self.prepared = True

    def makeAxis(self, i):
        grid = self.grid
        Axis = np.linspace(np.log10(grid[3 * i]), 
                np.log10(grid[3 * i + 1]), int(grid[3 * i + 2]))
        for AxisLimits, j in zip([self.args.xl, self.args.yl], [0, 1]):
            if j == i and AxisLimits:
                xl = np.log10(AxisLimits)
                xInd = [np.where(Axis >= xl[0])[0].min(), 
                        np.where(Axis <= xl[1])[0].max() + 1]
                Axis = Axis[Axis >= xl[0]]
                Axis = Axis[Axis <= xl[1]]
                self.axisInd[i] = xInd
        self.axis[i] = Axis.copy()

    @classmethod
    def saver(cls, ndim, name):
        path = cls.args.output
        dirpath = os.path.dirname(path)
        basename = os.path.basename(path)
        path = "{}/{:02}_{}D_{}_{}".format(dirpath, cls.k, ndim, name, basename)
        cls.k += 1
        plt.savefig(path, dpi=450)
        print(path+" saved")

    def prepareData(self):
        data = []
        xInd, yInd = self.axisInd.values()
        CLs = self.CLs[yInd[0]:yInd[1], xInd[0]:xInd[1]]
        success = self.success[yInd[0]:yInd[1], xInd[0]:xInd[1]]
        if self.args.contour:
            self.contour = self.contour[yInd[0]:yInd[1], xInd[0]:xInd[1]]
        data.append(np.ma.array(CLs[:,:,0], mask=False))
        for k in range(3):
            if self.args.log:
                data.append(np.log10(np.ma.array(CLs[:,:, 2 + k],
                    mask=np.invert(success[:,:,k]))))
            else:
                data.append(np.ma.array(CLs[:,:, 2 + k],
                    mask=np.invert(success[:,:,k])))
        self.data = np.ma.array(data)

    def plot2D(self, name, title):
        x, y = self.axis.values()
        fig = plt.figure()
        x, y = np.power(10, [x, y])
        xx, yy = np.meshgrid(x, y)
        if name == "CLs":
            cs = plt.contourf(xx, yy, self.data[0], cmap=cm.coolwarm)
        else:
            cs = plt.contourf(xx, yy, self.data[parDict.types[name] - 1],
                    cmap=cm.coolwarm)
        if self.args.contour:
            plt.contour(xx, yy, self.contour, 1 - self.args.contour)
        plt.xlabel(r"$\sin^2 2\theta_{14}$")
        plt.ylabel(r"$\Delta m^2_{41}$")
        plt.xscale('log')
        plt.yscale('log')
        plt.title(r"2D "+title+parDict.chi2_map[name])
        plt.colorbar(cs)
        plt.tight_layout()
    
    def plot3D(self, name, title):
        x, y = self.axis.values()
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        xx, yy = np.meshgrid(x, y)
        if name == "CLs":
            surf = ax.plot_surface(xx, yy, self.data[0], 
                    cmap=cm.coolwarm, linewidth=0, antialiased=False)
        else:
            surf = ax.plot_surface(xx, yy, self.data[parDict.types[name] - 1],
                    cmap=cm.coolwarm, linewidth=0, antialiased=False)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
        ax.set_title(r"3D "+title+parDict.chi2_map[name])
    
        plt.xlabel(r"$\log_{10} ( \sin^2 2\theta_{14}$ )")
        plt.ylabel(r"$\log_{10} ( \Delta m^2_{41} )$")
    
        fig.colorbar(surf, shrink=0.5, aspect=5)
        plt.tight_layout()


    def plotter(self, name, title):
        if not self.prepared:
            self._prepare()
        if self.args.D2:
            self.plot2D(name, title)
            if self.args.output:
                self.saver(2, name)

        if self.args.D3:
            self.plot3D(name, title)
            if self.args.output:
                self.saver(3, name)
 

