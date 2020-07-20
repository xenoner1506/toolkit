import numpy as np
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-s', default='~/software/gna/scripts/tmp.sh',
        help='path to save script')
parser.add_argument('-o', type=str, default='AD11', help='observable')
parser.add_argument('-p', type=str, default='SinSqDouble14', help='paramenter')
parser.add_argument('-f', type=str, nargs=2, default=['DeltaMSq14', '1.e-2'], 
        help='fixed parameter')
parser.add_argument('-l', type=float, nargs=2, default=[-4, 0], help='limits')
args = parser.parse_args()

pars_dict = {'DeltaMSq14': "$\Delta m^2_{41}$", "SinSqDouble14": "$\sin^2 2\theta_{14}$"}

command = "./gna \\\n"
command += "\t-- exp --ns H0 dayabay \\\n"
command += "\t-- exp --ns H1 dayabay --sterile \\\n"
command += "\t-- spectrum --plot-type hist -p H0/{} -l 'H0' \\\n".format(args.o)
command += "\t-- ns --name H1.pmns --print \\\n"
command += "\t --set {} values={} \\\n".format(*args.f)

for x in np.logspace(args.l[0], args.l[1], num=5, base=10):
    command += "\t\t-- ns --name H1.pmns --print \\\n"
    command += "\t\t --set {} values={} \\\n".format(args.p, x)
    command += "\t\t-- spectrum --plot-type hist -p H1/{} -l ".format(args.o)
    command += "'{} ={:1.2e}' \\\n".format(args.p, x)

command += "-- mpl -g -s -t '{}: {} = {}'".format(args.o, pars_dict[args.f[0]], args.f[1])

with open(args.s, "w") as f:
    f.write(command)


