"""
Colors copied from https://github.com/IAMconsortium/pyam/blob/main/pyam/plotting.py
"""

PYAM_COLORS = {
    # AR6 colours from https://github.com/IPCC-WG1/colormaps
    # where each file is processed to generate hex values, e.g.:
    # with open('rcp_cat.txt') as f:
    #   for l in f.readlines():
    #     rgb = np.array([int(x) for x in l.strip().split()]) / 256
    #     print(matplotlib.colors.rgb2hex(rgb))
    "AR6-SSP1": "#1e9583",
    "AR6-SSP2": "#4576be",
    "AR6-SSP3": "#f11111",
    "AR6-SSP4": "#e78731",
    "AR6-SSP5": "#8036a7",
    "AR6-SSP1-1.9": "#00acce",
    "AR6-SSP1-2.6": "#173c66",
    "AR6-SSP2-4.5": "#f69320",
    "AR6-SSP3-7.0": "#e61d25",
    "AR6-SSP3-LowNTCF": "#e61d25",
    "AR6-SSP4-3.4": "#63bce4",
    "AR6-SSP4-6.0": "#e78731",
    "AR6-SSP5-3.4-OS": "#996dc8",
    "AR6-SSP5-8.5": "#941b1e",
    "AR6-RCP-2.6": "#980002",
    "AR6-RCP-4.5": "#c37900",
    "AR6-RCP-6.0": "#709fcc",
    "AR6-RCP-8.5": "#003466",
    # AR5 colours from
    # https://tdaviesbarnard.co.uk/1202/ipcc-official-colors-rcp/
    "AR5-RCP-2.6": "#0000FF",
    "AR5-RCP-4.5": "#79BCFF",
    "AR5-RCP-6.0": "#FF822D",
    "AR5-RCP-8.5": "#FF0000",
}
