"""
Plotting phenoll 2 data for mind and life SRI poster
This one is dream traits (other main fig is waking correlates)
"""
import numpy as np
import pandas as pd
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


EXPORT_FNAME = '../results/sri-phenoll2_plot-dreamstuff.png'

# from excel sheet
poslo = [9,9,7,12,9,10,9,15,6,6,6,16]
poshi = [20,20,20,3,26,14,26,6,6,11,15,15]
bizlo = [5,3,2,10,4,5,5,9,5,1,4,2]
bizhi = [7,7,7,8,10,7,9,6,5,1,5,10]


yvals, yerr = zip(*[ ( np.mean(vals), sem(vals) ) 
                    for vals in [poslo,poshi,bizlo,bizhi] ])

xvals = [0,1,3,4]
COLORS = dict(lo='gainsboro',hi='cornflowerblue')
color_seq = [ COLORS[c] for c in ['lo','hi','lo','hi'] ]

# legend
STROKE_WIDTH = .6
FONT_SIZE = 18
LEFT_PAD = .02
# FONT_PAD = .055

BARWIDTH = .7

fig, ax = plt.subplots(figsize=(7,5))

ax.bar(xvals,yvals,yerr=yerr,color=color_seq,width=BARWIDTH,
       edgecolor='k',linewidth=2,
       error_kw={'ecolor'     : 'k',
                 'elinewidth' : 2,
                 'capsize'    : 2,
                 'capthick'   : 2},
       zorder=1)

POINT_OFFSET = .1
points_xvals = [ xvals[0]+POINT_OFFSET, xvals[1]-POINT_OFFSET,
                 xvals[2]+POINT_OFFSET, xvals[3]-POINT_OFFSET ]

LINEWIDTH = .5
for y1, y2, y3, y4 in zip(poslo,poshi,bizlo,bizhi):
    ax.plot(points_xvals[:2],[y1,y2],'-',
            color='k',alpha=1,linewidth=LINEWIDTH,zorder=2)
    ax.scatter(points_xvals[:2],[y1,y2],s=25,c=color_seq[:2],alpha=1,
               linewidth=LINEWIDTH,edgecolor='k',zorder=3)
    ax.plot(points_xvals[2:],[y3,y4],'-',color='k',alpha=1,
            linewidth=LINEWIDTH,zorder=2)
    ax.scatter(points_xvals[2:],[y3,y4],s=25,c=color_seq[2:],alpha=1,
               linewidth=LINEWIDTH,edgecolor='k',zorder=3)

ax.set_ylim(0,32)
ax.set_xlim(-1,5)
# ax.xaxis.set_major_locator(plt.NullLocator())
ax.set_xticks([ np.mean(xvals[:2]), np.mean(xvals[2:]) ])
ax.set_xticklabels([ 'Positive emotions\nwhile dreaming', 'Dream bizarreness' ],fontsize=16)
ax.xaxis.set_ticks_position('none')

ax.yaxis.set(major_locator=mticker.MultipleLocator(30),
             minor_locator=mticker.MultipleLocator(10))
ax.set_ylabel("Subjective rating" + #r"$\bf{Waking\ mood\ the\ next\ day}$"
              "\nless $\leftarrow$                                     $\\rightarrow$ more",
              labelpad=5,
              fontsize=14)


# ttest = pg.ttest(poslo,poshi,paired=True)
# ttest = pg.ttest(bizlo,bizhi,paired=True)

pval_txt = "$\it{p}$ = .05"
effs_txt = "$\it{d}$ = 1.03"
ax.text(.63,32,pval_txt,fontsize=12,va='center',ha='left')
ax.text(.63,30.7,effs_txt,fontsize=12,va='center',ha='left')
ax.text(np.mean(xvals[:2]),28.53,'*',fontsize=30,va='center',ha='center')
ax.hlines(y=28,xmin=xvals[0],xmax=xvals[1],linewidth=2,color='k',capstyle='round')

pval_txt = "$\it{p}$ < .05"
effs_txt = "$\it{d}$ = 0.87"
ax.text(3.63,16,pval_txt,fontsize=12,va='center',ha='left')
ax.text(3.63,14.7,effs_txt,fontsize=12,va='center',ha='left')
ax.text(np.mean(xvals[2:]),12.53,'*',fontsize=30,va='center',ha='center')
ax.hlines(y=12,xmin=xvals[2],xmax=xvals[3],linewidth=2,color='k',capstyle='round')

ax.text(1,1,'Dreams with low lucidity',
        color=COLORS['lo'],fontsize=FONT_SIZE,
        ha='right',va='top',
        transform=ax.transAxes,
        rotation=0,
        path_effects=[mpatheffects.withStroke(linewidth=STROKE_WIDTH,foreground='k')])
ax.text(1,.93,'Dreams with high lucidity',
        color=COLORS['hi'],fontsize=FONT_SIZE,
        ha='right',va='top',
        transform=ax.transAxes,
        rotation=0,
        path_effects=[mpatheffects.withStroke(linewidth=STROKE_WIDTH,foreground='k')])


plt.tight_layout()
plt.savefig(EXPORT_FNAME)
plt.close()

