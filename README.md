# delta-sigma-py
Some models of Delta-Sigma ADC modulators in Python + Matplotlib

Implemented:
* 1st-Order 
* 2nd-Order
* MASH-1-1
* MASH-2-1

Hitting the reset button will reload the `modulators.py` module,
so a small bit of live-coding can happen without having to kill and
reload the Matplotlib window.

FFTs are 2048 samples. The frequency slider is in cycles-per-FFT window.
There's no window on the FFT, so try to select a prime number of 
cycles per window for the best-looking FFTs.

To Do
---------------
* Scale internal waveforms better
* Plot a zoom-in of the baseband
* Calculate the SNR over the baseband
* Allow to store a previous FFT, and plot with the
  latest for easy comparasons

