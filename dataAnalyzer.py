from yahoo_finance import Share
from scipy import stats
import math
import datetime
import helpers

def processPERatio(PERatio, paramList = [1, -1, 40, 0, 1]):
    #  Scale PE Ratio
    if (PERatio is not None):
        PERatio = paramList[0] + paramList[1] / math.exp(float(PERatio) / paramList[2])
        PERatio = helpers.clamp(PERatio, paramList[3], paramList[4])
    else:
        print "Could not retrieve PE ratio."
        PERatio = 0
    return PERatio

def processPEGRatio(PEGRatio, paramList = [2, 2, 0, 1]):
    # Scale PEG Ratio
    if (PEGRatio is not None):
        PEGRatio = (paramList[0] - float(PEGRatio)) / paramList[1]
        # Clamp PEG Ratio
        PEGRatio = helpers.clamp(PEGRatio, paramList[2], paramList[3])
    else:
        print "Could not retrieve PEG ratio."
        PEGRatio = 0
    return PEGRatio

def processShortRatio(ShortRatio, paramList = [1, -1, 5, 0, 1]):
    # Scale Short Ratio
    if (ShortRatio is not None):
        ShortRatio = paramList[0] + paramList[1] / math.exp(float(ShortRatio) / paramList[2])
        ShortRatio = helpers.clamp(ShortRatio, paramList[3], paramList[4])
    else:
        print "Could not retrieve short ratio."
        ShortRatio = 0
    return ShortRatio

def processHistorical(historical, paramList = [-7, 7, 7, 14, 5]):
    # Process historical data
    if (historical is not None):
        # Clamp historical price change between -4% and +4%
        historical = helpers.clamp(historical, paramList[0], paramList[1])
        historical = (historical + paramList[2]) / paramList[3] + math.sin(historical / paramList[4])
    else:
        print "Could not retrieve historical data."
        historical = 0
    return historical
