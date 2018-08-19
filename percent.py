


# encoding: utf-8
"""
This is the python code for the calculations. To build the workflow, I just
copy & paste this code into Alfred.

Supported Calculations:

1. Percent Change (increase/decrease): `% 3 6` -> 100%
2. Percentage of; 3 is what percent of 100: `% 3 of 100` -> 3%
3. Percent of: 5 percent of 100 is 5: `% 5 percent of 100` -> 5, or `% 5% of 100` -> 5
4. Percent Decrease; What is 2 percent from 100: `% 100 - 2%`
5. Percent Increase; What is 100 + 2%: `% 100 + 2%`
6. Original number before Percent Decrease; What number is 100 2 percent less than?:`% 100 is 2% lt`
7. Original number before Percent Increase; What number is 100 2 percent more than?:`% 100 is 2% gt`
"""

__version__ = "1.5.1"
import sys
import types
from workflow import Workflow, ICON_INFO


def percent_increase(a, b):
    """What is `a` + `b`%?"""
    return str(round(a + (a * (b / 100.0)), 2))


def percent_decrease(a, b):
    """What is `a` - `b`%?"""
    return str(round(a - (a * (b / 100.0)), 2))


def percentage_of(a, b):
    """`a` of `b` is what percent?"""
    return "{0}%".format(str(round((a / b) * 100, 2)))


def percent_of(a, b):
    """Calculates `a` percent of `b` is what percent?"""
    return str(round((a / 100.0) * b, 2))


def percent_change(a, b):
    """Given two floats, calculate the percent change and return a rounded
    string representation of the change."""
    if a > 0:
        result = ((b - a) / a) * 100
    else:
        result = 0
    return str(round(result, 2))


def before_percent_decrease(a, b):
    """What is `a` `b`% less than"""
    percent = b / 100.0 
    result = a / (1 - percent)
    return str(round(result, 2))


def before_percent_increase(a, b):
    """What is `a` `b`% more than"""
    percent = b / 100
    result = a * (1 - percent)
    return str(round(result, 2))


def parse(args):
    """Inspects the input arguments and calls the correct function.

    Returns a Tuple:
        (the calculated value, a human-readable version of the function used)

    """
    try:
        values = ''
        if len(args) == 1 and type(args) == list:
            values = args[0].strip().split(' ')

        if len(values) == 2:
            # `% a b`. percent_change.
            result = percent_change(float(values[0]), float(values[1]))
            return (result, 'Percent Change')

        elif len(values) == 4 and 'percent' in values and 'of' in values:
            # `% a percent of b`. percent_of
            a = float(values[0])
            b = float(values[-1])
            result = percent_of(a, b)
            return (result, 'Percentage of')

        elif len(values) == 3 and values[0].endswith("%"):
            # `% a% of b`. percent_of
            a = float(values[0].strip("%"))
            b = float(values[-1])
            result = percent_of(a, b)
            return (result, 'Percentage of')

        elif len(values) == 3 and 'of' in values:
            # `% a of b`.percentage_of
            a = float(values[0])
            b = float(values[-1])
            result = percentage_of(a, b)
            return (result, 'Percentage of')

        elif len(values) == 3 and '-' in values:
            # `% a - b%`. percent_decrease
            a = float(values[0])
            b = float(values[-1].replace("%", ""))
            result = percent_decrease(a, b)
            return (result, 'Percent decrease')

        elif len(values) == 3 and '+' in values:
            # `% a + b%`. percent_increase
            a = float(values[0])
            b = float(values[-1].replace("%", ""))
            result = percent_increase(a, b)
            return (result, 'Percent increase') 

        elif (len(values) == 3 or len(values) == 4) and 'lt' in values:
            # `% a is b% lt` . original_number_before_decrease
            # `is` verb optional 
            a = float(values[0])
            b = float(values[-2].replace("%", ""))
            result = before_percent_decrease(a, b)
            return (result, 'Before decrease')

        elif (len(values) == 3 or len(values) == 4) and 'gt' in values:
            # `% a is b% lt` . original_number_before_decrease
            # `is` verb optional 
            a = float(values[0])
            b = float(values[-2].replace("%", ""))
            result = before_percent_increase(a, b)
            return (result, 'Before increase')

        elif len(values) == 1 and "help" in values:
            # `% help`
            return [
                ("Increase / Decrease:", "% 3 6"),
                ("Add/Subtract:", "% 100 + 2%"),
                ("Percentage of:", "% 3 of 100"),
                ("Num before % increase:", "% 100 is 2% gt"),
                ("Num before % decrease:", "% 100 is 2% lt"),
            ]
    
        else:
            return ("What?", "I don't know what you mean.")
    except ValueError:
        return ("What?", "...")


def main(wf):
    results = parse(wf.args)
    if isinstance(results, types.TupleType):
        title, subtitle = results
        wf.add_item(title=title, subtitle=subtitle, arg=title)

    elif isinstance(results, types.ListType):
        results = parse(wf.args)
        for i in results:
            title, subtitle = i
            wf.add_item(title=title, subtitle=subtitle, arg=title)

    wf.send_feedback()  # Send results back to Alfred as XML

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


def test_percent_increase():
    _eq(percent_increase(100.0, 2.0), "102.0")
    _eq(percent_increase(12.34, 2.0), "12.59")
    _eq(percent_increase(12.34, 2.5), "12.65")
    _eq(percent_increase(14.0, 2.0), "14.28")


def test_percent_decrease():
    _eq(percent_decrease(100.0, 2.0), "98.0")
    _eq(percent_decrease(12.34, 2.0), "12.09")
    _eq(percent_decrease(12.34, 2.5), "12.03")
    _eq(percent_decrease(14.0, 2.0), "13.72")


def test_percentage_of():
    _eq(percentage_of(3.0, 100.00), "3.0%")
    _eq(percentage_of(2.0, 5.0), "40.0%")
    _eq(percentage_of(5.0, 3.0), "166.67%")


def test_percent_of():
    _eq(percent_of(3, 10), "0.3")
    _eq(percent_of(100, 10), "10.0")
    _eq(percent_of(5, 100), "5.0")
    _eq(percent_of(110, 3), "3.3")


def test_percent_change():
    _eq(percent_change(3.0, 6.0), "100.0")
    _eq(percent_change(5.0, 2.0), "-60.0")
    _eq(percent_change(3.5, 3.52), "0.57")


def test_before_percent_decrease():
    _eq(before_percent_decrease(3.0, 2), "3.06")
    _eq(before_percent_decrease(5.0, 1.5), "5.08")
    _eq(before_percent_decrease(2000, 4.6), "2096.44")


def test_before_percent_increase():
    _eq(before_percent_increase(3.0, 2), "2.94")
    _eq(before_percent_increase(5.0, 1.5), "4.92")
    _eq(before_percent_increase(2000, 4.6), "1908.0")

def test_parse():
    _eq(parse("3 6"), "100.0")  # percent_change
    _eq(parse("2 of 5"), "40.0")  # percentage_of
    _eq(parse("100 - 2%"), "98.0")  # percent_decrease
    _eq(parse("100 + 2%"), "102.0")  # percent_increase
    _eq(parse("100 is 2% lt"), "102.04")  # before_percent_decrease
    _eq(parse("100 is 2% gt"), "98.0")  # before_percent_decrease


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "test":
        print("Running Tests:\n")
        test_percent_increase()
        test_percent_decrease()
        test_percentage_of()
        test_percent_of()
        test_percent_change()
        print("\n\nDone.")
        if len(FAILURES):
            print("ERRORS:")
            print("\n{0}\n".format("\n".join(FAILURES)))
    else:
        wf = Workflow(libraries=['./lib'])
        # uncomment to log via log.debug(var)
        # log = wf.logger 
        sys.exit(wf.run(main))


