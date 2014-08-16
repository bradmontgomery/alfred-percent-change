"""
This is the python code for the calculations. To build the workflow, I just
copy & paste this code into Alfred.

Supported Calculations:

1. Percent Change (increase/decrease): `% 3 6` -> 100%
2. Percent of; What is 3 percent of 100: `% 3 of 100` -> 3%
3. Percent Difference; What is 2 percent from 100: `% 100 - 2%`
"""
import sys


def percent_difference(a, b):
    """What is `a` - `b`%?"""
    return str(round(a - (a * (b / 100.0)), 2))


def percent_of(a, b):
    """What is `a` percent of `b`?"""
    return str(round((a / b) * 100, 2))


def percent_change(a, b):
    """Given two floats, calculate the percent change and return a rounded
    string representation of the change."""
    if a > 0:
        result = ((b - a) / a) * 100
    else:
        result = 0
    return str(round(result, 2))


def parse(input_string):
    """Parses the input string and hands off the values to the correct function."""
    values = input_string.strip().split(' ')
    if len(values) == 2:
        # `% a b`. percent_change.
        return percent_change(float(values[0]), float(values[1]))
    elif len(values) == 3 and 'of' in values:
        # `% a of b`. percent_of
        a = float(values[0])
        b = float(values[-1])
        return percent_of(a, b)
    elif len(values) == 3 and '-' in values:
        # `% a - b%`. percent_difference
        a = float(values[0])
        b = float(values[-1].replace("%", ""))
        return percent_difference(a, b)
    else:
        return "What?"

# -----------------------------------------------------------------------------
# Some Tests. To run these, do:
#
# $ python script.py test
#
# (yes, I reinvented a wheel, here)
# -----------------------------------------------------------------------------
FAILURES = []


def _eq(a, b):
    global FAILURES
    try:
        assert a == b
    except AssertionError:
        sys.stderr.write("F")
        FAILURES.append("{0} is not equal to {1}".format(a, b))
    else:
        sys.stdout.write(".")


def test_percent_difference():
    _eq(percent_difference(100.0, 2.0), "98.0")
    _eq(percent_difference(12.34, 2.0), "12.09")
    _eq(percent_difference(12.34, 2.5), "12.03")
    _eq(percent_difference(14.0, 2.0), "13.72")


def test_percent_of():
    _eq(percent_of(3.0, 100.00), "3.0")
    _eq(percent_of(2.0, 5.0), "40.0")
    _eq(percent_of(5.0, 3.0), "166.67")


def test_percent_change():
    _eq(percent_change(3.0, 6.0), "100.0")
    _eq(percent_change(5.0, 2.0), "-60.0")
    _eq(percent_change(3.5, 3.52), "0.57")


def test_parse():
    _eq(parse("3 6"), "100.0")  # percent_change
    _eq(parse("2 of 5"), "40.0")  # percent_of


if __name__ == "__main__":
    if sys.argv[0] == "-c":  # Getting run by alfred.
        sys.stdout.write(parse('{query}'))

    elif len(sys.argv) == 2 and sys.argv[1] == "test":
        print("Running Tests:\n")
        test_percent_difference()
        test_percent_of()
        test_percent_change()
        print("\n\nDone.")
        if len(FAILURES):
            print("ERRORS:")
            print("\n{0}\n".format("\n".join(FAILURES)))
