numeral_to_value = {
    "M": 1000,
    "D": 500,
    "C": 100,
    "L": 50,
    "X": 10,
    "V": 5,
    "I": 1
}


def numeral_to_arabic(numeral_str):
    numeral_str = numeral_str.upper()
    val = 0
    for i in range(len(numeral_str) - 1):
        # get numerals and check they are valid
        numeral = numeral_str[i]
        next_numeral = numeral_str[i + 1]
        if numeral not in numeral_to_value:
            raise ValueError("numeral_str has invalid numeral: " + numeral)
        if next_numeral not in numeral_to_value:
            raise ValueError("numeral_str has invalid numeral: " + next_numeral)
        # figure out whether adding or subtracting for digits before last
        if numeral_to_value[numeral] < numeral_to_value[next_numeral]:
            val -= numeral_to_value[numeral]
        else:
            val += numeral_to_value[numeral]
    # always add last digit
    val += numeral_to_value[numeral_str[-1]]
    return val
