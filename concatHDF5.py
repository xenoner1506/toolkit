import os
import h5py
import numpy as np

files = os.listdir('./')
DATA = dict()

zero_keys = ['H0', 'H1']
first_keys = ['toyMC']
second_keys = ['errors', 'x']

for name in files:
    if name.endswith('.hdf5'):
        base, _ = name.split('.')
        _, num = base.split('_')

        with h5py.File(name, 'r') as f:
            for key0 in zero_keys:
                for key1 in first_keys:
                    key = '/'.join([key0, key1])
                    key_chi2 = '/'.join([key, 'chi2'])
                    if not DATA.get(key_chi2):
                        DATA[key_chi2] = []
                    DATA[key_chi2] += [ f[key_chi2][()] ]
                    for key2 in second_keys:
                        key_par = '/'.join([key0, key1, key2])
                        for point in f[key_par].keys():
                            key_point = '/'.join([key_par, point])
                            if not DATA.get(key_point):
                                DATA[key_point] = []
                            DATA[key_point] += [ f[key_point][()] ]

with h5py.File('FC_total.hdf5', 'w') as f:
    for key in DATA.keys():
        f.create_dataset(key, data=np.hstack(DATA[key]))

