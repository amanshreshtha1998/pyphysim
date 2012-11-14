#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Implements a waterfilling method.

The doWF method performs the waterfilling algorithm.
"""

import numpy as np


def doWF(vtChannels, dPt, noiseVar=1.0, Es=1.0):
    """Performs the Waterfilling algorithm and returns the optimum power and water level.

    Arguments:
    - `vtChannels`: Numpy array with the channel POWER gains (power of the
                    parallel AWGN channels).
    - `dPt`: Total available power.
    - `noiseVar`: Noise variance (power in linear scale)
    - `Es`: Symbol energy (in linear scale)
    """
    ## Sort Channels (descending order)
    vtChannelsSortIndexes = np.argsort(vtChannels)[::-1]
    vtChannelsSorted = vtChannels[vtChannelsSortIndexes]

    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # Calculates the water level that touches the worst channel (the higher
    # one) and therefore transmits zero power in this worst channel. After
    # that, calculates the power in each channel (the vector 'Ps') for this
    # water level. If the sum of all of these powers in 'Ps' is less then
    # the total available power, then all we need to do is divide the
    # remaining power equally among all the channels (increase the water
    # level). On the other hand, if the sum of all of these powers in 'Ps'
    # is greater then the total available power then we remove the worst
    # channel and repeat the process.
    # xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    # Calculates minimum waterlevel $\mu$ required to use all channels
    dNChannels = vtChannels.size
    dRemoveChannels = 0

    minMu = float(noiseVar) / (
        Es * vtChannelsSorted[dNChannels - dRemoveChannels - 1])
    Ps = (minMu - float(noiseVar) / (
        Es * vtChannelsSorted[np.arange(0, dNChannels - dRemoveChannels)]))

    while (sum(Ps) > dPt) and (dRemoveChannels < dNChannels):
        dRemoveChannels = dRemoveChannels + 1
        minMu = float(noiseVar) / (
            Es * vtChannelsSorted[dNChannels - dRemoveChannels - 1])
        Ps = (minMu - float(noiseVar) / (
            Es * vtChannelsSorted[np.arange(0, dNChannels - dRemoveChannels)]))

    # Distributes the remaining power among the all the remaining channels
    dPdiff = dPt - Ps.sum()
    vtOptPaux = dPdiff / (dNChannels - dRemoveChannels) + Ps

    # Put optimum power in the original channel order
    vtOptP = np.zeros([vtChannels.size, ])
    vtOptP[vtChannelsSortIndexes[np.arange(0, dNChannels - dRemoveChannels)]] = vtOptPaux
    mu = vtOptPaux[0] + float(noiseVar) / vtChannelsSorted[0]

    return (vtOptP, mu)
