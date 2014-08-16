"""
This is the python code for the calculations. To build the workflow, I just
copy & paste this code into Alfred.

Supported Calculations:

1. Percent Change (increase/decrease): `% 3 6` -> 100%

"""
import sys


def calculate_percent_change(a, b):
    """Given two floats, calculate the percent change and return a rounded
    string representation of the change."""
    if a > 0:
        result = ((b - a) / a) * 100
    else:
        result = 0
    return str(round(result, 2))


def parse(input_string):
    """Parses the input string and hands off the values to the correct function."""
    values = [float(v) for v in input_string.strip().split(' ')]
    if len(values) == 2:
        # We got `% a b`, calculate percent change.
        return calculate_percent_change(values[0], values[1])

# -----------------------------------------------------------------------------
# Some Tests. To run these, do:
#
# $ python script.py test
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


def test_calculate_percent_change():
    _eq(calculate_percent_change(3.0, 6.0), "100.0")
    _eq(calculate_percent_change(5.0, 2.0), "-60.0")
    _eq(calculate_percent_change(3.5, 3.52), "0.57")


if __name__ == "__main__":
    if sys.argv[0] == "-c":  # Getting run by alfred.
        sys.stdout.write(parse('{query}'))

    elif len(sys.argv) == 2 and sys.argv[1] == "test":
        print("Running Tests:\n")
        test_calculate_percent_change()
        print("\n\nDone.")
        if len(FAILURES):
            print("ERRORS:")
            print("\n{0}\n".format("\n".join(FAILURES)))
