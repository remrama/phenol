"""
Plotting phenoll 2 data for mind and life SRI poster
"""
import numpy as np
import pingouin as pg

from scipy.stats import sem

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patheffects as mpatheffects

from matplotlib import rcParams
rcParams['savefig.dpi'] = 300
rcParams['interactive'] = True
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = 'Arial'
rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False


EXPORT_FNAME = './phenoll2plot-TEST.svg'

# from excel sheet
lo = [13,16,14,11,31,23,25,13,12,10,11,19]
hi = [30,40,35,15,35,31,36,11,10,23,17,19]
ttest = pg.ttest(lo,hi,paired=True)

yvals, yerr = zip(*[ ( np.mean(vals), sem(vals) ) for vals in [lo,hi] ])

xvals = [0,1]
COLORS = dict(lo='gainsboro',hi='cornflowerblue')

color_seq = [ COLORS[c] for c in ['lo','hi'] ]

# legend
STROKE_WIDTH = .6
FONT_SIZE = 15
LEFT_PAD = .02
# FONT_PAD = .055

BARWIDTH = .7

fig, ax = plt.subplots(figsize=(4,5))

ax.bar(xvals,yvals,yerr=yerr,color=color_seq,width=BARWIDTH,
       edgecolor='k',linewidth=2,
       error_kw={'ecolor'     : 'k',
                 'elinewidth' : 2,
                 'capsize'    : 2,
                 'capthick'   : 2},
       zorder=1)

points_xvals = [ xvals[0]+.1, xvals[1]-.1 ]

LINEWIDTH = .5
for y1, y2 in zip(lo,hi):
    ax.plot(points_xvals,[y1,y2],'-',color='k',alpha=1,
            linewidth=LINEWIDTH,zorder=2)
    ax.scatter(points_xvals,[y1,y2],s=25,c=color_seq,alpha=1,
               linewidth=LINEWIDTH,edgecolor='k',zorder=3)

ax.set_ylim(0,50)
ax.set_xlim(-1,2)
ax.xaxis.set_major_locator(plt.NullLocator())
ax.yaxis.set(major_locator=mticker.MultipleLocator(50),
             minor_locator=mticker.MultipleLocator(10))
ax.set_ylabel('Positive waking mood')


pval_txt = "$\it{p}$ < .01"
effs_txt = "$\it{d}$ = 1.02"
# effs_txt = "$\it{ES}_{d}$ = 1.02"
# ax.text(.5,1,pval_txt,fontsize=9,va='top',ha='center',transform=ax.transAxes)
# ax.text(.5,1-.05,effs_txt,fontsize=9,va='top',ha='center',transform=ax.transAxes)
ax.text(.63,49,pval_txt,fontsize=12,va='center',ha='left')
ax.text(.63,47,effs_txt,fontsize=12,va='center',ha='left')
ax.text(.5,43.3,'*',fontsize=30,va='center',ha='center')
ax.hlines(y=43,xmin=0,xmax=1,linewidth=2,color='k',capstyle='round')



ax.text(xvals[0]-(BARWIDTH/2+.15),.7,'Mornings after low lucidity',
        color=COLORS['lo'],fontsize=FONT_SIZE,
        va='bottom',ha='right',
        # transform=ax.transAxes,
        rotation=90,
        path_effects=[mpatheffects.withStroke(linewidth=STROKE_WIDTH,foreground='k')])
ax.text(xvals[1]+(BARWIDTH/2+.15),.7,'Mornings after high lucidity',
        color=COLORS['hi'],fontsize=FONT_SIZE,
        va='bottom',ha='left',
        # transform=ax.transAxes,
        rotation=90,
        path_effects=[mpatheffects.withStroke(linewidth=STROKE_WIDTH,foreground='k')])




# ax.text(0+LEFT_PAD,1.,'Morning after dreams with',
#         color='white',fontsize=FONT_SIZE,
#         va='top',ha='left',transform=ax.transAxes,
#         path_effects=[mpatheffects.withStroke(linewidth=STROKE_WIDTH,foreground='k')])
# ax.text(0+LEFT_PAD,.93,'            low lucidity',
#         color=COLORS['lo'],fontsize=FONT_SIZE,
#         va='top',ha='left',transform=ax.transAxes,
#         path_effects=[mpatheffects.withStroke(linewidth=STROKE_WIDTH,foreground='k')])
# # lo_txt = r"$\bf{\ \ \ \ \ \ \ \ \ \ \ \ high\ lucidity}$"
# lo_txt = '            high lucidity'
# ax.text(0+LEFT_PAD,.86,lo_txt,
#         color=COLORS['hi'],fontsize=FONT_SIZE,
#         va='top',ha='left',transform=ax.transAxes,
#         path_effects=[mpatheffects.withStroke(linewidth=STROKE_WIDTH,foreground='k')])


plt.tight_layout()
plt.savefig(EXPORT_FNAME)
plt.close()





