import matplotlib.pyplot as plt
import numpy as np
import importlib

from matplotlib.collections import LineCollection
from matplotlib.ticker import MultipleLocator

from matplotlib.widgets import Slider, Button, RadioButtons
import modulators

N = 2048
R = 3.0
OSR = 32

fig = plt.figure("Delta Sigma")

# set up time series array
dt = 0.01
Tmax = N * 1.10 * dt
t = np.arange(0.01, Tmax, dt)
f0 = R / ( N * dt)

# sub-plots
fig.subplots_adjust(bottom=0.25, left=0.1)
ax2 = fig.add_subplot(2,1,2) # waveforms
ax3 = fig.add_subplot(2,2,1) # FFT of bitstream
ax4 = fig.add_subplot(2,2,2) # misc for now

axcolor = 'lightgoldenrodyellow'
axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
axamp = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
axreset = plt.axes([0.8, 0.025, 0.1, 0.04])

freq_slider = Slider(axfreq, 'Freq', 1, 31, valinit=3)
amp_slider = Slider(axamp, 'Amp', 0.1, 1.0, valinit=0.8)
button = Button(axreset, 'Reset', color=axcolor, hovercolor='0.975')

def _snr(mg_spec, mg_freqs, osr):
    """ Get SNR in basband """
    # input is single-sided
    # assume coherent input signal so power in 1 bin
    N = len(mg_spec)
    print(N)
    bwi = int(np.ceil(N/osr))

    boi_spec = mg_spec[:bwi]
    total_power = boi_spec ** 2.0

    # signal
    signal_index = np.argmax(total_power)
    signal_power = total_power[signal_index]

    # noise
    total_power[signal_index] = 0.0
    noise_power = sum(total_power)

    # SNR
    f_bw = mg_freqs[bwi]
    snr = 20.0 * np.log10(signal_power/noise_power)
    return f_bw, snr


def update(val):

    # clear
    ax2.clear()
    ax3.clear()
    ax4.clear()

    # get new values from sliders
    freq = freq_slider.val / (N * dt)
    amp = amp_slider.val

    # recompute input signal
    s1 = amp * np.sin(2 * freq * np.pi * t)

    # run the modulator over the time series
    data, names = modulators.run(t, s1)
    numSamples, numRows = len(t), len(data)
    print("Samples:", numSamples)

    # plot the modulator 
    tick_locations = []
    ax2.set_xlim(0, Tmax)
    dmin = -2 #data.min()
    dmax = 2 #data.max()

    delta_row = (dmax - dmin) * 0.7  # Crowd them a bit.
    y0 = dmin
    y1 = (numRows - 1) * delta_row + dmax

    curves = []
    for i in range(numRows):
        data_with_offset = data[i] + (i*delta_row)
        curves.append( ax2.step(t, data_with_offset, linewidth=0.5) )
        tick_locations.append( i*delta_row)

    # Set the yticks to use axes coordinates on the y axis
    ax2.set_ylim(y0, y1)
    ax2.set_yticks(tick_locations)
    ax2.set_yticklabels(names)
    ax2.set_xlabel('Time (s)')

    # FFT
    spec_data = data[-1][-N:]
    assert( len(spec_data) == N )
    (ms_spec, ms_freqs, _ ) = ax3.magnitude_spectrum(
        spec_data,
        Fs=1.0/dt,
        window = np.ones(spec_data.shape),
        scale='dB',
        linewidth=0.4)
    ax3.set_ylim(-140, 0)
    ax3.set_xscale('log')

    f_bw, snr = _snr(ms_spec, ms_freqs, OSR)
    ax3.axvline(x=f_bw, alpha=0.75, color='lightgrey', zorder=0)
    title = "SNR = {:0.2f}dB, OSR = {}".format(snr, OSR)
    ax3.set_title(title)

    # z
    x1 = np.arange(len(spec_data))
    ax4.step(x1, spec_data)

def reset(event):
    importlib.reload(modulators)
    freq_slider.reset()
    amp_slider.reset()
    update(0)

# wire signals
freq_slider.on_changed(update)
amp_slider.on_changed(update)
button.on_clicked(reset)

# show
update(0)
#plt.tight_layout()
plt.show()
