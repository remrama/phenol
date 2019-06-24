"""
Import at top of any plot scripts to change
defaults and keep colormaps etc consistent.
"""
import matplotlib
import matplotlib.pyplot


# change default parameters
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = 'Arial'
matplotlib.rcParams['axes.labelsize'] = 'x-large'
matplotlib.rcParams['xtick.labelsize'] = 'large'
matplotlib.rcParams['ytick.labelsize'] = 'large'
matplotlib.rcParams['xtick.major.size'] = 5
matplotlib.rcParams['ytick.major.size'] = 5
matplotlib.rcParams['legend.fontsize'] = 'small'
matplotlib.rcParams['legend.title_fontsize'] = 'medium'
matplotlib.rcParams['savefig.dpi'] = 300
# matplotlib.rcParams['svg.fonttype']


#########  color map and legend stuff  #########

dlqmin, dlqspan = 1, 4
cmap = matplotlib.pyplot.cm.get_cmap('Blues')
dlqcolor = lambda x: cmap((x-dlqmin)/dlqspan)

NORECALL_COLOR = 'gainsboro'
DLQ_STRINGS = {
    1: 'Not at all',
    2: 'Just a little',
    3: 'Moderately',
    4: 'Pretty much',
    5: 'Very much',
}

dlqpatches = [ matplotlib.patches.Patch(
                                facecolor=dlqcolor(x),
                                label=f'{label}',
                                edgecolor='k')
               for x, label in DLQ_STRINGS.items() ]

norecall_patch = matplotlib.patches.Patch(
                                facecolor=NORECALL_COLOR,
                                label='No recall',edgecolor='k')
