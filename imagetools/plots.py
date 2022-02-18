import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import mpl_scatter_density # adds projection='scatter_density'
from matplotlib.colors import LinearSegmentedColormap


def apu_calc(data1, data2):
    """
    This function compute APU metrics.
    :param data1: Array of pixel values of a single band.
    :param data2: Array of pixel values of a single band.
    """
    assert data1.size == data2.size
    sample_size = data1.size

    residuals = data2 - data1

    acc = residuals.sum()/sample_size

    diff_a = np.power((residuals - acc), 2)
    prec = np.sqrt(diff_a.sum()/(sample_size-1))

    residuals_square = numpy.power(residuals, 2)
    unc = numpy.sqrt(residuals_square.sum()/sample_size)

    res_unc = 100 * (unc/data1.mean())

    return sample_size, acc, prec, unc, res_unc


def plot_scatter_metrics(x, y, xlim=(0, 10000), ylim=(0, 10000), cmap=None):
    if x.ndim > 1:
        x = np.ravel(x)
    if y.ndim > 1:
        y = np.ravel(x)

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    r2 = r_value**2

    # "Viridis-like" colormap with white background
    white_viridis = LinearSegmentedColormap.from_list('white_viridis', [
        (0, '#ffffff'),
        (1e-20, '#440053'),
        (0.2, '#404388'),
        (0.4, '#2a788e'),
        (0.6, '#21a784'),
        (0.8, '#78d151'),
        (1, '#fde624'),
    ], N=256)
    if cmap is None:
        cmap = white_viridis

    fig = plt.figure()

    ax = fig.add_subplot(1, 1, 1, projection='scatter_density')
    density = ax.scatter_density(x, y, cmap=cmap)

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    fig.colorbar(density, label='Number of points per pixel')

    # Main Diagonal
    main_diag = np.array([min(xlim[0], ylim[0]), max(xlim[0], ylim[0])])
    plt.plot(main_diag, main_diag, color='#808080', ls='dashed', linewidth=1)

    # Text Box
    textstr = f" n={x.shape[0]}\n R = {r_value:.4f} \n {'${R^2}$'} = {r2:.4f} \n stderr = {std_err:.4f} \n intercept={intercept:.4f}\n slope={slope:.4f}"
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.01)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=11, verticalalignment='top', bbox=props)

    plt.show()
