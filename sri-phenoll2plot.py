"""
Plotting phenoll 2 data for mind and life SRI poster
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


EXPORT_FNAME = '../results/sri-phenoll2_plot.png'

# from excel sheet
df = pd.DataFrame({
        'subj' : range(12),
        'wakepos_lo' : [13,16,14,11,31,23,25,13,12,10,11,19],
        'wakepos_hi' : [30,40,35,15,35,31,36,11,10,23,17,19],
        'wakeneg_lo' : [16,17,10,12,16,28,20,20,11,19,24,12],
        'wakeneg_hi' : [10,10,10,32,16,25,14,27,12,12,15,16],
        'dreampos_lo' : [9,9,7,12,9,10,9,15,6,6,6,16],
        'dreampos_hi' : [20,20,20,3,26,14,26,6,6,11,15,15],
        'dreamneg_lo' : [23,21,8,18,8,18,15,21,7,19,15,3],
        'dreamneg_hi' : [8,20,14,30,7,20,9,16,6,4,8,7],
        'sleepq_lo' : [3,5,5,4,3,2,4,3,6,5,2,7],
        'sleepq_hi' : [4,5,4.5,2,5,2,5,6,6,4,4,4],
        'biz_lo' : [5,3,2,10,4,5,5,9,5,1,4,2],
        'biz_hi' : [7,7,7,8,10,7,9,6,5,1,5,10],
    })

# ttest = pg.ttest(neglo,neghi,paired=True)

poslo = [13,16,14,11,31,23,25,13,12,10,11,19]
poshi = [30,40,35,15,35,31,36,11,10,23,17,19]
neglo = [16,17,10,12,16,28,20,20,11,19,24,12]
neghi = [10,10,10,32,16,25,14,27,12,12,15,16]
posdreamlo = [9,9,7,12,9,10,9,15,6,6,6,16]
posdreamhi = [20,20,20,3,26,14,26,6,6,11,15,15]
negdreamlo = [23,21,8,18,8,18,15,21,7,19,15,3]
negdreamhi = [8,20,14,30,7,20,9,16,6,4,8,7]
slpquallo = [3,5,5,4,3,2,4,3,6,5,2,7]
slpqualhi = [4,5,4.5,2,5,2,5,6,6,4,4,4]
bizlo = [5,3,2,10,4,5,5,9,5,1,4,2]
bizhi = [7,7,7,8,10,7,9,6,5,1,5,10]


yvals, yerr = zip(*[ ( np.mean(vals), sem(vals) ) 
                    for vals in [poslo,poshi,neglo,neghi] ])

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
for y1, y2, y3, y4 in zip(poslo,poshi,neglo,neghi):
    ax.plot(points_xvals[:2],[y1,y2],'-',
            color='k',alpha=1,linewidth=LINEWIDTH,zorder=2)
    ax.scatter(points_xvals[:2],[y1,y2],s=25,c=color_seq[:2],alpha=1,
               linewidth=LINEWIDTH,edgecolor='k',zorder=3)
    ax.plot(points_xvals[2:],[y3,y4],'-',color='k',alpha=1,
            linewidth=LINEWIDTH,zorder=2)
    ax.scatter(points_xvals[2:],[y3,y4],s=25,c=color_seq[2:],alpha=1,
               linewidth=LINEWIDTH,edgecolor='k',zorder=3)

ax.set_ylim(0,50)
ax.set_xlim(-1,5)
# ax.xaxis.set_major_locator(plt.NullLocator())
ax.set_xticks([ np.mean(xvals[:2]), np.mean(xvals[2:]) ])
ax.set_xticklabels([ 'Positive mood', 'Negative mood' ],fontsize=16)
ax.xaxis.set_ticks_position('none')

ax.yaxis.set(major_locator=mticker.MultipleLocator(50),
             minor_locator=mticker.MultipleLocator(10))
ax.set_ylabel('Waking mood')
ax.set_ylabel("Waking mood the next day" + #r"$\bf{Waking\ mood\ the\ next\ day}$"
              "\nworse $\leftarrow$                                     $\\rightarrow$ better",
              labelpad=5,
              fontsize=14)


pval_txt = "$\it{p}$ < .01"
effs_txt = "$\it{d}$ = 1.02"
# effs_txt = "$\it{ES}_{d}$ = 1.02"
# ax.text(.5,1,pval_txt,fontsize=9,va='top',ha='center',transform=ax.transAxes)
# ax.text(.5,1-.05,effs_txt,fontsize=9,va='top',ha='center',transform=ax.transAxes)
ax.text(.63,49,pval_txt,fontsize=12,va='center',ha='left')
ax.text(.63,47,effs_txt,fontsize=12,va='center',ha='left')
ax.text(np.mean(xvals[:2]),43.3,'*',fontsize=30,va='center',ha='center')
ax.hlines(y=43,xmin=xvals[0],xmax=xvals[1],linewidth=2,color='k',capstyle='round')

ax.text(np.mean(xvals[2:]),35.3,'n.s.',fontsize=12,va='bottom',ha='center',weight='bold')
ax.hlines(y=35,xmin=xvals[2],xmax=xvals[3],linewidth=2,color='k',capstyle='round')


ax.text(1,1,'Mornings after low lucidity',
        color=COLORS['lo'],fontsize=FONT_SIZE,
        ha='right',va='top',
        transform=ax.transAxes,
        rotation=0,
        path_effects=[mpatheffects.withStroke(linewidth=STROKE_WIDTH,foreground='k')])
ax.text(1,.93,'Mornings after high lucidity',
        color=COLORS['hi'],fontsize=FONT_SIZE,
        ha='right',va='top',
        transform=ax.transAxes,
        rotation=0,
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





