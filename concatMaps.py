import os
import h5py
import numpy as np
import pylib.parDict as parDict
from argparse import ArgumentParser
from matplotlib import pyplot as plt
from pylib.nameParser import nameParse
from pylib.plot_lines import plot_lines



def main():
    parser = ArgumentParser()
    parser.add_argument('-o', '--output', help='path/to/save/plot')
    parser.add_argument('-p', '--paths', nargs='*', help='path/to/hdf5')
    parser.add_argument('-l', '--labels', nargs='*', help='labels of lines')
    parser.add_argument('-t', '--types', nargs='*', 
            help='types that printed to lines box')
    parser.add_argument('-s', '--show', action='store_true', help='show figure')
    parser.add_argument('--extra', nargs='*', action='append', default=[],
            help='extra labels in legend')
    args = parser.parse_args()


    if args.paths:
        paths = args.paths
    else:
        paths = os.listdir('./')

    print(paths)
    CLs = []
    for path, clr in zip(paths, parDict.clrs):
        fileDict = nameParse(path)
        with h5py.File(path, 'r') as f:
            fileDict['clr'] = clr
            fileDict['map'] = f['CL\'s'][:]
            fileDict['grid'] = f['grid'][:]
        CLs.append(fileDict)
    
    CS = []
    labels = []
    if args.types:
        fig, axs = plt.subplots(figsize=(8.5, 6.5))
    else:
        fig, axs = plt.subplots(figsize=(7.5, 6.5))
    
    for i, path in enumerate(args.paths):
        grid = CLs[i]['grid']
        x = np.linspace(np.log10(grid[0]), np.log10(grid[1]), int(grid[2]))
        x = np.power(10, x)
        y = np.linspace(np.log10(grid[3]), np.log10(grid[4]), int(grid[5]))
        y = np.power(10, y)
        xx, yy = np.meshgrid(x, y)
    
        if args.extra:
            for pair in args.extra:
                if str(i) == pair[0]:
                    CS.append(axs.contour(xx, yy, 
                        np.zeros((int(grid[2]), int(grid[5]))), colors='white'))
                    labels.append(pair[1])
                    print(pair[1], pair)
    
        CS.append(axs.contour(xx, yy, CLs[i]['map'][:,:,0], [0.05],
            colors=CLs[i]['clr']))
        
        labels.append(args.labels[i])
   
    plt.legend([cs.collections[0] for cs in CS], labels, loc='upper left')
    
    lines = []
    if args.types:
        for key in args.types:
            if key in parDict.par_dict:
                for line in parDict.par_dict[key]:
                    lines.append(line)
                lines.append([''])
        plot_lines(lines, loc='lower left')
        plt.xlim((6.e-5, 1.))
    
    plt.grid(which='minor', linestyle='--')
    plt.grid(which='major', linestyle='-')
    plt.xscale('log')
    plt.yscale('log')
    
    plt.xlabel(r'$\sin^2 2\theta_{14}$')
    plt.ylabel(r'$\Delta m^2_{41}$')
    plt.title(r'Daya Bay, 90% $CL_s$')
    
    plt.tight_layout()
    
    if args.output:
        plt.savefig(args.output, dpi=450)
    if args.show:
        plt.show()


if __name__ == '__main__':
    main()



