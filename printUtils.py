from math import floor
def printTime(timeSeconds=0):
    if timeSeconds == 0:
        return None
    out = ''

    if timeSeconds >= 1:
        s = floor(timeSeconds)
        out += str(s) + 's '
        timeSeconds -= s

    timeSeconds = timeSeconds * 10 ** 3

    if timeSeconds >= 1:
        ms = floor(timeSeconds)
        out += str(ms) + 'ms '
        timeSeconds -= ms

    timeSeconds = timeSeconds * 10 ** 3
    
    if timeSeconds >= 1:
        us = floor(timeSeconds)
        out += str(us) + 'us '
        timeSeconds -= us

    timeSeconds = timeSeconds * 10 ** 3

    if timeSeconds >= 1:
        ns = floor(timeSeconds)
        out += str(ns) + 'ns'

    print(out)