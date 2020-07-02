import os
import h5py
import numpy as np
from matplotlib import cm
from argparse import ArgumentParser
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import LinearLocator, FormatStrFormatter


parser = ArgumentParser()
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

data_type = {"CLs": 0, "H0_DATA": 1, "H1_DATA": 2, "H0_H1": 3, "H1_H0": 4}

names = {"CLs": r'$CL_s$', "H0_DATA": r'$\chi^2_{H_0}(DATA)$',
        "H1_DATA": r'$\chi^2_{H_1}(DATA)$', 
        "H0_H1": r'$\chi^2_{H_0}(H_1)$',
        "H1_H0": r'$\chi^2_{H_1}(H_0)$'}

def makeGrid(grid):
    x = np.linspace(np.log10(grid[0]), np.log10(grid[1]), int(grid[2]))
    if args.xl:
        xInd = [np.where(x >= xl[0])[0].min(), np.where(x <= xl[1])[0].max() + 1]
        x = x[x >= xl[0]]
        x = x[x <= xl[1]]
        print(xInd)
    else:
        xInd = []
    y = np.linspace(np.log10(grid[3]), np.log10(grid[4]), int(grid[5]))
    if args.yl:
        yInd = [np.where(y >= yl[0])[0].min(), np.where(y <= yl[1])[0].max() + 1]
        y = y[y >= yl[0]]
        y = y[y <= yl[1]]
        print(yInd)
    else:
        yInd = []
    return x, y, xInd, yInd


def saver(k, ndim, name):
    path = args.output
    path = "{:02}_{}D_{}_{}".format(k, ndim, name, path)
    plt.savefig(path, dpi=450)
    print(path+" saved")


def plot2D(x, y, data, name, title):
    fig = plt.figure()
    x = np.power(10, x)
    y = np.power(10, y)
    xx, yy = np.meshgrid(x, y)
    cs = plt.contourf(xx, yy, data, cmap=cm.coolwarm)
    plt.xlabel(r"$\sin^2 2\theta_{14}$")
    plt.ylabel(r"$\Delta m^2_{41}$")
    plt.xscale('log')
    plt.yscale('log')
    plt.title(r"2D "+title+names[name])
    plt.colorbar(cs)
    plt.tight_layout()


def plot3D(x, y, data, name, title):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    xx, yy = np.meshgrid(x, y)
    surf = ax.plot_surface(xx, yy, data, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    ax.set_title(r"3D "+title+names[name])

    plt.xlabel(r"$\log_{10} ( \sin^2 2\theta_{14}$ )")
    plt.ylabel(r"$\log_{10} ( \Delta m^2_{41} )$")

    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.tight_layout()


def plotter(types, x, y, title, key0, key1=None, xind=None, yind=None):
    if key1:
        pre_data = CLs[key0]['map'] - CLs[key1]['map']
    else:
        pre_data = CLs[key0]['map']
    if xind:
        pre_data = pre_data[:,xind[0]:xind[1],:]
    if yind:
        pre_data = pre_data[yind[0]:yind[1],:,:]
    for i, name in enumerate(types):
        if args.log and i != 0:
            data = np.log10(pre_data[:,:,i])
        else:
            data = pre_data[:,:,i]
        if args.D2:
            plot2D(x, y, data, name, title)
            if args.output:
                saver(i, 2, name)

        if args.D3:
            plot3D(x, y, data, name, title)
            if args.output:
                saver(i, 3, name)

CLs = dict()
pathes = args.pathes

if args.types:
    types = args.types
else:
    types = ["CLs", "H0_DATA", "H1_DATA", "H0_H1", "H1_H0"]

for path in args.pathes:
    for filename in os.listdir(path):
        if filename.endswith('.hdf5') and "CLs" in filename:
            key = path.split('/')[-1]
            CLs[key] = dict()
            with h5py.File(path+'/'+filename, 'r') as f:
                CLs[key]['map'] = f['CL\'s'][:]
                CLs[key]['grid'] = f['grid'][:]

if args.xl:
    xl = np.log10(args.xl)
if args.yl:
    yl = np.log10(args.yl)

if args.df:
    key0 = args.pathes[0].split('/')[-1]
    key1 = args.pathes[1].split('/')[-1]
    x, y, xInd, yInd = makeGrid(CLs[key0]['grid'])

    plotter(types, x, y, "Difference map of ", key0, key1, xInd, yInd)
else:
    for path in args.pathes:
        key = path.split('/')[-1]
        x, y, xInd, yInd = makeGrid(CLs[key]['grid'])
       
        plotter(types, x, y, "Map of ", key, xind=xInd, yind=yInd)

if args.show:
    plt.show()   


