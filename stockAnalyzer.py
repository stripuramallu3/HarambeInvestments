from yahoo_finance import Share
from scipy import stats
import math
import datetime

def growthProbability(stockName):
    stock = Share(stockName)

    weightPE = 0.01
    weightPEG = 0.01
    weightShort = 0.01
    weightHistorical = 0.01

    PERatio = stock.get_price_earnings_ratio()
    #  Scale PE Ratio
    if (PERatio is not None):
        PERatio = 1 - 1 / math.exp(float(PERatio) / 40)
        weightPE = 0.15
    else:
        print "Could not retrieve PE ratio."
        PERatio = 0

    PEGRatio = stock.get_price_earnings_growth_ratio()
    # Scale PEG Ratio
    if (PEGRatio is not None):
        PEGRatio = (2 - float(PEGRatio)) / 2
        # Clamp PEG Ratio
        PEGRatio = clamp(PEGRatio, 0, 1)
        weightPEG = 0.3
    else:
        print "Could not retrieve PEG ratio."
        PEGRatio = 0

    ShortRatio = stock.get_short_ratio()
    # Scale Short Ratio
    if (ShortRatio is not None):
        ShortRatio = 1 - 1 / math.exp(float(ShortRatio) / 5)
        weightShort = 0.15
    else:
        print "Could not retrieve short ratio."
        ShortRatio = 0

    try:
        historical = getFiveDaySlope(stockName)
        # Scale 5 day slope
        historical = float(historical) / float(stock.get_price()) * 100
        # Clamp historical price change between -100% and +5%
        historical = clamp(historical, -5, 5)
        historical = historical / 5 + math.sin(historical / 5)
        weightHistorical = 0.4
    except:
        print "Could not retrieve historical data."
        historical = 0

    probability = (PERatio * weightPE + PEGRatio * weightPEG + ShortRatio * weightShort + historical * weightHistorical) / (weightPE + weightPEG + weightShort + weightHistorical)
    return probability

def getFiveDaySlope(stockName):
    # Initialize values.
    stock = Share(stockName)
    x = []
    y = []
    # Get a range of dates.
    endDate = datetime.datetime.now().strftime("%Y-%m-%d")
    startDate = (datetime.datetime.now() - datetime.timedelta(days = 8)).strftime("%Y-%m-%d")
    # Get only the last 5 business days.
    historicalData = stock.get_historical(startDate, endDate)
    historicalData = historicalData[-5:]
    # Create a graph where the x axis is 0 - 4.5 and the y axis is open and close prices
    for i in range(5):
        x += [5.5 - i, 5.5 - (i + float(1) / 2)]
        y += [float(historicalData[i]['Open']), float(historicalData[i]['Close'])]
    x += [0.5, 0]
    y = [float(stock.get_price()), float(stock.get_price())] + y
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    return slope

def clamp(value, lowerBound, upperBound):
    if value < lowerBound:
        value = lowerBound
    elif value > upperBound:
        value = upperBound
    return value