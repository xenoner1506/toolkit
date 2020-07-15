types = {"CLs": 0, "H0_DATA": 1, "H1_DATA": 2, "H0_H1": 3, "H1_H0": 4}

chi2_map = {"CLs": r'$CL_s$', "H0_DATA": r'$\chi^2_{H_0}(DATA)$',
        "H1_DATA": r'$\chi^2_{H_1}(DATA)$', "H0_H1": r'$\chi^2_{H_0}(H_1)$',
        "H1_H0": r'$\chi^2_{H_1}(H_0)$'}

par_names = {"baseline": r'L', "fission_fraction_corr": r'f', 
        "eper_fission": r'$E^{fission}$', "spectral_weights": r"S_{i}",
        "nominal_thermal_power": r'$W_{th}$', "snf_scale": r'SNF',
        "eres": r'$\sigma_{E}$', "lsnl_weight": r'LSNL',
        "escale": r'$E_{scale}$', "fastn_shape": r'$S($fast $n)$',
        "acc_norm": r'$N^{acc}$', "bkg_rate_fastn": r'$N^{bkg}($fast $n)$',
        "bkg_rate_amc": r'$N^{bkg}($AmC$)$', "bkg_rate_alphan": r'$N^{bkg}($C($\alpha$, n)$)$',
        "bkg_rate_lihe": r"$N^{bkg}($Li / He$)$", "effunc_uncorr": r'$\epsilon$',
        "offeq_scale": r'off equilibrium', "OffdiagScale": r"IAV"}

legend_dict = {"all": "TOTAL", "bkg": 'stats.+background', 
        "ad_reactor_energy": 'stats.+ad+reactor+energy', 
        "ad_reactor": 'stats.+ad+reactor', "ad": 'stats.+ad', "free2": 'free osc', 
        "free3": 'free osc, norm', "free4": 'free osc, norm', 
        "systs": r"Stats.+syst.", "stats": r"Stats. only",
        "higher": r"Higher order",
        "effunc_uncorr": r'$\epsilon$', "eper_fission": r'$E^{fission}$',
        "offeq_scale": r'$Eq^{off}_{scale}$', "bkg_rate_lihe": r'$R^{bkg}(Li/He)$',
        "acc_norm": r'$N^{acc}$', "fission_fraction_corr": r'$R^{fission}_{corr}$',
        "lsnl_weight": r'$w_{lsnl}$', "eres": r'$R_{E}$', 
        "escale": r'E_{scale}', "bkg_rate_alphan": r'$C^{bkg}(\alpha, n)$',
        "OffdiagScale": r'$IAV_{scale}$', "fastn_shape": r'$S^{fast}_{shape}(n)$',
        "bkg_rate_fastn": r'$R^{bkg}_{fast}(n)$',
        "nominal_thermal_power": r'$W^{nominal}_{tp}$', 
        "frac_li": r'$R^{bkg}(Li/He)$',
        "bkg_rate_amc": r'$R^{bkg}(AmC)$', 'far': r'Large $\Delta m^2_{14}$'}

par_dict = {"all": ["TOTAL:", r"AD+REACTOR+ENERGY+BACKGROUND"],
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


