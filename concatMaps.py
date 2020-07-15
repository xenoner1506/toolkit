import os
import h5py
import numpy as np
from argparse import ArgumentParser
from matplotlib import pyplot as plt
from mpl_tools.plot_lines import plot_lines


legend_dict = {"all": "TOTAL", "bkg": 'stats.+background', 
        "ad_reactor_energy": 'stats.+ad+reactor+energy', 
        "ad_reactor": 'stats.+ad+reactor', "ad": 'stats.+ad', "free2": 'free osc', 
        "free3": 'free osc, norm', "free4": 'free osc, norm', 
        "baseline_5": r"$\sigma_{baseline}$ = 5",
        "baseline_4": r"$\sigma_{baseline}$ = 4",
        "baseline_3": r"$\sigma_{baseline}$ = 3",
        "baseline_2": r"$\sigma_{baseline}$ = 2",
        "baseline_1": r"$\sigma_{baseline}$ = 1",
        "systs": r"Stats.syst.",
        "stats": r"Stats. only",
        "higher": r"Higher order",
        "effunc_uncorr": r'$\epsilon$', 
        "eper_fission": r'$E^{fission}$',
        "offeq_scale": r'$Eq^{off}_{scale}$', 
        "bkg_rate_lihe": r'$R^{bkg}(Li/He)$',
        "acc_norm": r'$N^{acc}$', 
        "fission_fraction_corr": r'$R^{fission}_{corr}$',
        "lsnl_weight": r'$w_{lsnl}$', "eres": r'$R_{E}$', 
        "escale": r'E_{scale}', "bkg_rate_alphan": r'$C^{bkg}(\alpha, n)$',
        "OffdiagScale": r'$IAV_{scale}$', "fastn_shape": r'$S^{fast}_{shape}(n)$',
        "bkg_rate_fastn": r'$R^{bkg}_{fast}(n)$',
        "nominal_thermal_power": r'$W^{nominal}_{tp}$', 
        "frac_li": r'$R^{bkg}(Li/He)$',
        "bkg_rate_amc": r'$R^{bkg}(AmC)$', 'far': r'Large $\Delta m^2_{14}$'}

pars_dict = {"all": ["TOTAL:", r"AD+REACTOR+ENERGY+BACKGROUND"],
        "ad_reactor": ["REACTOR:", r"$f,\ E^{fission},\ W_{th},\ $off equlibrium, SNF"],
        "ad_reactor_energy": ["ENERGY:", r"$\sigma_{E},\ $LSNL, IAV"],
        "bkg": ["BKG:", 
            r"$\omega^{Li},\ N^{bkg}(Li/He),\ N^{bkg}(AmC),\ N^{bkg}(C(\alpha, n)),$", 
            r"$N^{acc}, N^{bkg}($fast $n),\ S^{bkg}($fast $n)$"],
        "ad": ["AD:", r"$E_{scale},\ \epsilon$"],
        'free2': [r"Oscilation parameters: $\sin^22\theta_{13},\ \Delta m^2_{23}$"],
        'free3': [r"Antineutrino shape: $w_{i, spectral},\ i=\overline{1, 15}$"],
        'free4': [r"Global normalization: $N^{global}$"]}

clrs = ['black', 'blue', 'red', 'green', 'purple', 'brown', 'tan', 
        'darkgoldenrod', 'gold', 'olive', 'green', 'lime', 'turquoise', 'teal', 'cyan',
        'skyblue', 'navy', 'darkviolet', 'plum', 'purple', 'orchid', 'crimson', 'pink', 'peru']

parser = ArgumentParser()
parser.add_argument('-o', '--output', help='path/to/save/plot')
parser.add_argument('-p', '--pathes', nargs='*', help='path/to/hdf5')
parser.add_argument('-l', '--labels', nargs='*', help='labels of lines')
parser.add_argument('-t', '--types', nargs='*', 
        help='types that printed to lines box')
parser.add_argument('-s', '--show', action='store_true', help='show figure')
parser.add_argument('--extra', nargs='*', action='append', default=[],
        help='extra labels in legend')
args = parser.parse_args()


clr_dict = dict()
for path, clr in zip(args.pathes, clrs):
    key = path.split('/')[-1]
    clr_dict[key] = clr
clr_dict['far'] = 'black'


CLs = dict()
if args.pathes:
    pathes = args.pathes
else:
    pathes = os.listdir('./')

for path in args.pathes:
    print(path)
    for filename in os.listdir(path):
        print(filename)
        if filename.endswith('.hdf5') and "CLs" in filename:
            key = path.split('/')[-1]
            CLs[key] = dict()
            with h5py.File(path+'/'+filename, 'r') as f:
                CLs[key]['map'] = f['CL\'s'][:]
                CLs[key]['grid'] = f['grid'][:]


CS = []
labels = []
k = 0
if args.types:
    fig, axs = plt.subplots(figsize=(8.5, 6.5))
else:
    fig, axs = plt.subplots(figsize=(7.5, 6.5))

for i, path in enumerate(args.pathes):
    key = path.split('/')[-1]
    grid = CLs[key]['grid']
    x = np.linspace(np.log10(grid[0]), np.log10(grid[1]), int(grid[2]))
    x = np.power(10, x)
    y = np.linspace(np.log10(grid[3]), np.log10(grid[4]), int(grid[5]))
    y = np.power(10, y)
    xx, yy = np.meshgrid(x, y)

    if args.extra:
        for pair in args.extra:
            if key == pair[0]:
                CS.append(axs.contour(xx, yy, 
                    np.zeros((int(grid[2]), int(grid[5]))), colors='white'))
                labels.append(legend_dict[pair[1]])
                print(legend_dict[pair[1]], pair)
                k += 1

    CS.append(axs.contour(xx, yy, CLs[key]['map'][:,:,0], [0.05],
        colors=clr_dict[key]))
    
    if not args.labels:
        labels.append(legend_dict[key])
    else:
        labels.append(args.labels[i])

#if args.labels:
#    if labels:
#        labels += [value for value in args.labels]
#    else:
#        labels = [value for value in args.labels]


plt.legend([cs.collections[0] for cs in CS], labels, loc='upper left')

print(CS)
print(labels)

lines = []
if args.types:
    for key in args.types:
        if key in pars_dict:
            for line in pars_dict[key]:
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
