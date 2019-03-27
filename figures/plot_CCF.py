from imports import *
from scipy.stats import skewnorm, norm
from scipy.ndimage.filters import gaussian_filter

# define ccfs
xnorm = np.linspace(-7,7,500)
ccf = -1 * skewnorm.pdf(xnorm, 2)
sig = .7
normccf = .8*ccf.min() * norm.pdf(xnorm,0,sig) / norm.pdf(xnorm,0,sig).max()
x = xnorm - float(xnorm[abs(ccf-ccf.min()) == np.min(abs(ccf-ccf.min()))])

# compute fwhm and location
xhwhm = 2*np.sqrt(2*np.log(2)) * ccf[ccf<-.01].std()
yfwhm = float(ccf[abs(x-2*xhwhm) == np.min(abs(x-2*xhwhm))])
xfwhm = x[np.isclose(ccf, yfwhm, atol=.01)]
fwhmcol = '#0080ff'

# compute BIS over the line
Nbin = 10
Dccf = abs(ccf.min() - ccf.max()) / (Nbin-1.)
mids, bis = np.zeros(Nbin-1), np.zeros(Nbin-1)
for i in range(Nbin-1):
    g = (ccf >= ccf.min()+i*Dccf) & (ccf <= ccf.min()+(i+1)*Dccf) & \
        (ccf <= -.001)
    mids[i] = ccf[g].mean()
    bis[i] = x[g].mean()
bis = gaussian_filter(bis,2)
bisint = interp1d(bis, mids, bounds_error=False, fill_value=np.nan)
biscol = '#33DF09'#35EA09'

# compute contrast
xcon = x[(x<0) & (ccf>-.005)].mean()
xcon = np.append(xcon, x[(x>0) & (ccf>-.005)].mean())
xcon2 = [x[ccf==ccf.min()]]
ycon = np.zeros(2)
ycon2 = [ccf.min()]
concol = '#F52F07'

# plotting
fig = plt.figure(figsize=(10,3.5))
ax1 = fig.add_subplot(131)
ax1.plot(xnorm, normccf, 'k:', lw=2, label='Gaussian CCF')
ax1.plot(x, ccf, 'k-', lw=2, label='Observed CCF\n(noiseless)')
ax1.set_xlim((x.min(),x.max()))
ax1.set_ylim((-.62,.025))
ax1.axis('off')
ax1.plot(xfwhm, np.repeat(yfwhm,2), '-', lw=4, c=fwhmcol)#, label='FWHM')
#ax1.text(0, -.67, 'Velocity', horizontalalignment='center')
ax1.text(-7.7, -.3, 'CCF', horizontalalignment='center', rotation=90)
ax1.plot(np.zeros(2), [-.55,-.62], 'k-')
ax1.text(0, -.66, 'V$_0$', fontsize=12, horizontalalignment='center')
ax1.set_title('FWHM', fontsize=12, color=fwhmcol, y=.97, weight='semibold')

ax2 = fig.add_subplot(132)
ax2.plot(xnorm, normccf, 'k:', lw=2)
ax2.plot(x, ccf, 'k-', lw=2)
g = np.where(np.isfinite(bisint(x)))[0]
#ax2.fill_between(x, np.repeat(bisint(x)[g][1]-.05,x.size),
#                np.repeat(bisint(x)[g][1]+.05,x.size), alpha=.2, color='k')
#ax2.fill_between(x, np.repeat(bisint(x)[g][-2]-.05,x.size),
#                np.repeat(bisint(x)[g][-2]+.05,x.size), alpha=.2, color='k')
ax2.plot(x, bisint(x), '-', c=biscol, lw=4)#, label='BIS')
ax2.scatter(x[g][np.array([1,-2])], bisint(x)[g][np.array([1,-2])], s=100,
            facecolor=biscol, edgecolor='k')
ax2.set_xlim((x.min(),x.max()))
ax2.set_ylim((-.62,.025))
ax2.axis('off')
ax2.plot(np.zeros(2), [-.55,-.62], 'k-')
ax2.text(0, -.66, 'V$_0$', fontsize=12, horizontalalignment='center')
ax2.text(0, -.718, 'Velocity', horizontalalignment='center')
ax2.set_title('BIS', fontsize=12, color=biscol, y=.97, weight='semibold')

ax3 = fig.add_subplot(133)
ax3.plot(xnorm, normccf, 'k:', lw=2)
ax3.plot(x, ccf, 'k-', lw=2)
ax3.scatter(xcon, ycon, s=140, facecolor=concol, edgecolor='k',
            marker='d')
ax3.scatter(xcon2, ycon2, s=140, facecolor=concol, edgecolor='k',
            marker='o')#, label='Contrast')
ax3.set_xlim((x.min(),x.max()))
ax3.set_ylim((-.62,.025))
ax3.axis('off')
#ax3.text(0, -.67, 'Velocity', horizontalalignment='center')
ax3.plot(np.zeros(2), [-.55,-.62], 'k-')
ax3.text(0, -.66, 'V$_0$', fontsize=12, horizontalalignment='center')
ax3.set_title('Contrast', fontsize=12, color=concol, y=.97, weight='semibold')

fig.legend(bbox_to_anchor=[.44,.63], fontsize=11)
fig.subplots_adjust(bottom=.142, left=.02, right=.98, top=.94)
plt.savefig('/Users/ryancloutier/Research/Thesis/thesis/figures/ccf.png')
plt.show()
