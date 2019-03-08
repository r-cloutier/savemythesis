from imports import *
from matplotlib.ticker import NullFormatter


def plot_transmittance(wl, trans, pltt=True, label=False):
    fig = plt.figure(figsize=(7,4))
    ax = fig.add_subplot(111)
    ax.plot(wl, trans, 'k-', lw=.5)
   
    # plot bands
    bands = ['U','B','V','R','I','Y','J','H','K$_{S}$']
    wlcen = [0.3531,0.4430,0.5537,0.6940,0.8781,1.0259,1.2545,1.6310,2.1498]
    wlwidth = [0.0657,0.0973,0.0890,0.2070,0.2316,0.1084,0.1548,0.2886,0.3209]
    cols = ['0D0217','3501E1','00BA09','F52002','AE0800','9A0701','7B0601','5A0401','2C0201']
    for i in range(len(bands)):
	ax.fill_between([wlcen[i]-wlwidth[i]*.5,wlcen[i]+wlwidth[i]*.5], 0, 1, alpha=.4, color='#%s'%cols[i])
	ax.text(wlcen[i], 1.02, bands[i], horizontalalignment='center')

    ax.set_xscale('log')
    ax.set_xlabel('Wavelength [$\mu$m]')
    ax.set_ylabel('Transmittance')
    ax.set_xlim((.35,2.5)), ax.set_ylim((0,1))
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xticks(np.append(np.arange(.4,1,.1), np.arange(1,3)))
    ax.set_xticklabels(['0.4','','0.6','','0.8','','1','2'])

    fig.subplots_adjust(bottom=.15, top=.94, right=.97, left=.09)
    if label:
	plt.savefig('transmittance.png')
    if pltt:
	plt.show()
    plt.close('all')


if __name__ == '__main__':
    # get transmittance data
    wl, trans = np.loadtxt('/Users/ryancloutier/Research/RVInformation/RVFollowupCalculator/InputData/tapas_000001.ipac', skiprows=24).T
    wl *= 1e-3   # nm -> microns
    plot_transmittance(wl, trans, label=1)
    print ''
