import random

# shift the input in a random direction by the percentage of the error
def RNG_Shift(inputVal, error):
    shift = random.uniform(-inputVal * error / 100, inputVal * error / 100)
    return inputVal + round(shift, 2)

# give a boolean outcome depending on the possibility
def RNG_Outcome(possibility):
    tempList = (True, False)
    weights = (possibility, 1 - possibility)
    return str(random.choices(tempList, weights))=='[True]'

# round the input in a desired way
def round(input, decimals=2):
    input = str(input)
    point = input.find('.')
    temp = input[0:point + decimals + 1]
    return float(temp)

