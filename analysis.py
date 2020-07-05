import os
import h5py
import numpy as np
from matplotlib import cm
from argparse import ArgumentParser
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter


data_type = {"CLs": 0, "H0_DATA": 1, "H1_DATA": 2, "H0_H1": 3, "H1_H0": 4}

names = {"CLs": r'$CL_s$', "H0_DATA": r'$\chi^2_{H_0}(DATA)$',
        "H1_DATA": r'$\chi^2_{H_1}(DATA)$', 
        "H0_H1": r'$\chi^2_{H_0}(H_1)$',
        "H1_H0": r'$\chi^2_{H_1}(H_0)$'}

parser = ArgumentParser()
parser.add_argument('-c', '--contour', type=float, help='plot contour of CLs')
parser.add_argument('-o', '--output', help='path/to/save/plot')
parser.add_argument('-p', '--pathes', nargs='*', help='path/to/hdf5')
parser.add_argument('-t', '--types', nargs='*', help='what to plot')
parser.add_argument('-l', '--log', action='store_true', help='logarithmic scale')
parser.add_argument('-s', '--show', action='store_true', help='show figure')
parser.add_argument('--D2', action='store_true', help='make 2D plots')
parser.add_argument('--D3', action='store_true', help='make 3D plots')
parser.add_argument('--df', action='store_true', help='difference between two datas')
parser.add_argument('--xl', type=float, nargs='*', help='xlim for 2D/3d plot')
parser.add_argument('--yl', type=float, nargs='*', help='ylim for 2D/3d plot')
args = parser.parse_args()

class DATA():
    k = 0

    def __init__(self, CLs_map, grid, success, contour=None):
        self.CLs = CLs_map
        self.grid = grid
        self.success = np.array((success + 1) % 2, dtype=bool)
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
        for AxisLimits, j in zip([args.xl, args.yl], [0, 1]):
            if j == i and AxisLimits:
                xl = np.log10(AxisLimits)
                xInd = [np.where(Axis >= xl[0])[0].min(), 
                        np.where(Axis <= xl[1])[0].max() + 1]
                Axis = Axis[Axis >= xl[0]]
                Axis = Axis[Axis <= xl[1]]
                self.axisInd[i] = xInd
        self.axis[i] = Axis.copy()
        print(self.axisInd, i)

    @classmethod
    def saver(cls, ndim, name):
        path = args.output
        path = "{:02}_{}D_{}_{}".format(cls.k, ndim, name, path)
        cls.k += 1
        plt.savefig(path, dpi=450)
        print(path+" saved")

    def prepareData(self):
        data = []
        xInd, yInd = self.axisInd.values()
        CLs = self.CLs[yInd[0]:yInd[1], xInd[0]:xInd[1]]
        success = self.success[yInd[0]:yInd[1], xInd[0]:xInd[1]]
        if args.contour:
            self.contour = self.contour[yInd[0]:yInd[1], xInd[0]:xInd[1]]
        data.append(np.ma.array(CLs[:,:,0], mask=False))
        for k in range(3):
            if args.log:
                data.append(np.log10(np.ma.array(CLs[:,:, 2 + k],
                    mask=success[:,:,k])))
            else:
                data.append(np.ma.array(CLs[:,:, 2 + k],
                    mask=success[:,:,k]))
        self.data = np.array(data)

    def plot2D(self, name, title):
        x, y = self.axis.values()
        fig = plt.figure()
        x, y = np.power(10, [x, y])
        xx, yy = np.meshgrid(x, y)
        if name == "CLs":
            cs = plt.contourf(xx, yy, self.data[0], cmap=cm.coolwarm)
        else:
            cs = plt.contourf(xx, yy, self.data[data_type[name] - 2],
                    cmap=cm.coolwarm)
        if args.contour:
            plt.contour(xx, yy, self.contour, 1 - args.contour)
        plt.xlabel(r"$\sin^2 2\theta_{14}$")
        plt.ylabel(r"$\Delta m^2_{41}$")
        plt.xscale('log')
        plt.yscale('log')
        plt.title(r"2D "+title+names[name])
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
            surf = ax.plot_surface(xx, yy, self.data[data_type[name] - 2],
                    cmap=cm.coolwarm, linewidth=0, antialiased=False)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
        ax.set_title(r"3D "+title+names[name])
    
        plt.xlabel(r"$\log_{10} ( \sin^2 2\theta_{14}$ )")
        plt.ylabel(r"$\log_{10} ( \Delta m^2_{41} )$")
    
        fig.colorbar(surf, shrink=0.5, aspect=5)
        plt.tight_layout()


    def plotter(self, name, title):
        if not self.prepared:
            self._prepare()
        if args.D2:
            self.plot2D(name, title)
            if args.output:
                self.saver(2, name)

        if args.D3:
            self.plot3D(name, title)
            if args.output:
                self.saver(3, name)
    

def main():
    DATA_dict = dict()
    pathes = args.pathes
    
    if args.types:
        types = args.types
    else:
        types = ["CLs", "H1_DATA", "H0_H1", "H1_H0"]
    
    for path in args.pathes:
        for filename in os.listdir(path):
            if filename.endswith('.hdf5') and "CLs" in filename:
                key = path.split('/')[-1]
                with h5py.File(path+'/'+filename, 'r') as f:
                    DATA_dict[key] = DATA(f['CL\'s'][:], f['grid'][:],
                            f['success'][:], f['CL\'s'][:][:,:,0])
   
    print(DATA_dict)

    if args.df:
        key0, key1 = DATA_dict.keys()
        data = DATA_dict[key0].CLs - DATA_dict[key1].CLs
        success = ((DATA_dict[key0].success.astype(int) + 1) % 2 +
                (DATA_dict[key0].success.astype(int) + 1) % 2) / 2
        DATA_df = DATA(data, DATA_dict[key0].grid, success, DATA_dict[key0].contour)
        for name in types:
            DATA_df.plotter(name, "Difference map of ")
    else:
        for DATAs in DATA_dict.values():
            for name in types:
                DATAs.plotter(name, "Map of ")
    
    if args.show:
        plt.show()   
    

if __name__ == '__main__':
    main()


