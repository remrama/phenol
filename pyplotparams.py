"""
Import at top of any plot scripts to change
defaults and keep colormaps etc consistent.
"""
import matplotlib
import matplotlib.pyplot


# change default parameters
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = 'Arial'
matplotlib.rcParams['axes.labelsize'] = 9
matplotlib.rcParams['xtick.labelsize'] = 7
matplotlib.rcParams['ytick.labelsize'] = 7
matplotlib.rcParams['xtick.major.size'] = 5
matplotlib.rcParams['xtick.minor.size'] = 3
matplotlib.rcParams['ytick.major.size'] = 5
matplotlib.rcParams['ytick.minor.size'] = 3
matplotlib.rcParams['savefig.dpi'] = 300
matplotlib.rcParams['svg.fonttype'] = 'none'


#########  color map and legend stuff  #########

dlqmin, dlqspan = 0, 4
cmap = matplotlib.pyplot.cm.get_cmap('Blues')
dlqcolor = lambda x: cmap((x-dlqmin)/dlqspan)

NORECALL_COLOR = 'gainsboro'
DLQ_STRINGS = {
    0: 'Not at all',
    1: 'Just a little',
    2: 'Moderately',
    3: 'Pretty much',
    4: 'Very much',
}

dlqpatches = [ matplotlib.patches.Patch(
                                facecolor=dlqcolor(x),
                                label=f'{label}',
                                edgecolor='k')
               for x, label in DLQ_STRINGS.items() ]

norecall_patch = matplotlib.patches.Patch(
                                facecolor=NORECALL_COLOR,
                                label='No recall',edgecolor='k')
