#!/usr/bin/env python3

"""Visualize sample data from modem and export to image file"""

import sys
import os

from ahoi.handlers.SamplePlotHandler import SamplePlotHandler

import numpy as np
import matplotlib.pyplot as plt


def plot_and_save(file):
    try:
        data = np.loadtxt(file)
    except:
        print("ERROR: Could not read file %s" % file)
        exit(1)

    # Preprocess data
    # Values are in the interval [-16384, 16383]
    data = data / 16384
    data = data - np.mean(data)
    data = data.tolist()  # PlotHandler expects a list

    # Get standard deviation before zero padding
    stddev = np.std(data)

    # Check if data length is power of 2 and pad with zeros
    opt_len = 1
    while opt_len < len(data):
        opt_len = opt_len * 2
    if len(data) != opt_len:
        print(
            "WARNING: Number of samples (%i) not power of 2 in %s" % (len(data), file)
        )
    nprepend = (opt_len - len(data)) // 2
    prepend = [0] * nprepend
    nappend = opt_len - len(data) - nprepend
    append = [0] * nappend
    data = prepend + data + append

    # Choose sensible file name for output file
    outfile = file
    if outfile.endswith(".dat") and len(outfile) > 4:
        outfile = outfile[:-4]
    outfile = outfile + ".png"

    # Inject data into plotting class
    sph = SamplePlotHandler()
    sph.numTotal = len(data)
    sph.data = data
    sph.plot()

    # Write the file name in the plot
    plottext = file
    ilast = file.rfind("/")
    if ilast != -1 and len(file) > 1:
        plottext = plottext[ilast + 1 :]
    sph.axs[0].text(1, 0.85, plottext)

    # Write the standard deviation in the plot
    sph.axs[0].text(1, 0.7, "std dev: %.3f" % stddev)

    sph.axs[0].grid(alpha=0.5)
    sph.axs[1].grid()

    # Save
    plt.savefig(outfile, dpi=200)
    plt.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: %s file.dat" % sys.argv[0])
        exit(1)
    for i, arg in enumerate(sys.argv):
        if i == 0:
            continue
        plot_and_save(arg)
