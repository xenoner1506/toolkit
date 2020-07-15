import os
import h5py
from pylib.DATA import DATA
from argparse import ArgumentParser
from matplotlib import pyplot as plt



def main():
    parser = ArgumentParser()
    parser.add_argument('-c', '--contour', type=float, help='plot contour of CLs')
    parser.add_argument('-o', '--output', help='path/to/save/plot')
    parser.add_argument('-p', '--paths', nargs='*', help='path/to/hdf5')
    parser.add_argument('-t', '--types', nargs='*', help='what to plot')
    parser.add_argument('-l', '--log', action='store_true', help='logarithmic scale')
    parser.add_argument('-s', '--show', action='store_true', help='show figure')
    parser.add_argument('--D2', action='store_true', help='make 2D plots')
    parser.add_argument('--D3', action='store_true', help='make 3D plots')
    parser.add_argument('--df', action='store_true', help='difference between two datas')
    parser.add_argument('--xl', type=float, nargs=2, help='xlim for 2D/3d plot')
    parser.add_argument('--yl', type=float, nargs=2, help='ylim for 2D/3d plot')
    args = parser.parse_args()

    DATA_dict = dict()
    DATA.args = args
    paths = args.paths
    
    if args.types:
        types = args.types
    else:
        types = ["CLs", "H1_DATA", "H0_H1", "H1_H0"]
    
    for path in args.paths:
        key = os.path.basename(path)
        with h5py.File(path, 'r') as f:
            DATA_dict[key] = DATA(f['CL\'s'][:], f['grid'][:], f['success'][:],
                    f['CL\'s'][:][:,:,0])
   
    print(DATA_dict)

    if args.df:
        key0, key1 = DATA_dict.keys()
        data = DATA_dict[key0].CLs - DATA_dict[key1].CLs
        success = (DATA_dict[key0].success.astype(int) + 
                DATA_dict[key0].success.astype(int)) / 2
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


