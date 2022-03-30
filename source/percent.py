#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Partly cloudy ⛅️  🌡️+43°F (feels +39°F, 22%) 🌬️0mph 🌑 Wed Mar 30 16:19:59 2022


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

Tests: To run the tests, run:

    python percent.py test

See the bottom of this file for more details.

"""

__version__ = "1.6"
import sys
import types
import json


def log(s, *args):
    if args:
        s = s % args
    print(s, file=sys.stderr)



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
        if len(args) == 2 and type(args) == list:
            values = args[1].strip().split(' ')

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


def main():
    result = {"items": []}
    results = parse(sys.argv)
    
    if isinstance(results, tuple):
        title, subtitle = results
        result["items"].append({
            "title": title,
            'subtitle': subtitle,
            'valid': True,
            'arg': title
                }) 
        


    elif isinstance(results, list):
        results = parse(sys.argv)
        
               
        for i in results:
            title, subtitle = i
            result["items"].append({
            "title": title,
            'subtitle': subtitle,
            'valid': True,
            'arg': title 
                }) 
        

    print (json.dumps(result))
    



if __name__ == "__main__":
    main()


