import random

def RNG_Shift(inputVal, error):
    shift = random.uniform(-inputVal * error / 100, inputVal * error / 100)
    return inputVal + round(shift,2)

def RNG_Outcome(possibility):
    tempList = (True, False)
    weights = (possibility, 1 - possibility)
    return random.choices(tempList, weights)
def round(input, decimals):
    input = input
    input = "{:.2f}".format(input)
    return float(input)