import sys


def calculate_percent_change(input_string):
    values = '{query}'.strip().split(' ')
    values = [float(v.strip()) for v in values]
    a, b = values[:2]
    if a > 0:
        result = ((b - a) / a) * 100
    else:
        result = 0
    return str(result)


sys.stdout.write(calculate_percent_change('{query}'))
