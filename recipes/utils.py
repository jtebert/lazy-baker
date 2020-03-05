import re
from fractions import Fraction


def format_ingredient_line(txt):
    '''
    Formats a single line of an ingredients list into Markdown for putting on the page
    :param txt: String line of text
    :return: Text in markdown form (to be turned into HTML by make_markdown)
    '''

    txt_split = txt.split()
    if len(txt_split) == 0:
        # This is a blank line
        pass
    elif len(txt) >= 2 and txt[0] == '[' and txt[-1] == ']':
        # This is a section marker
        txt = '### ' + txt[1:-1]
    else:
        number_part = ''
        # This is an ingredient line
        # Check if first values are numbers (will get decimals, fractions, and integers)
        ind = 0
        while is_number(txt_split[ind]) or txt_split[ind] == '-':
            ind += 1
        if ind > 0:
            number_part = ' '.join(txt_split[0:ind])
            txt_split = txt_split[ind:]

        # Check if first value is a number range (e.g., 6-8)
        try:
            lower, upper = txt_split[0].split('-')
            if is_number(lower) and is_number(upper):
                number_part = '{} - {}'.format(lower, upper)
                txt_split = txt_split[1:]
        except:
            pass

        # Check for units
        if is_unit(txt_split[0]):
            unit_part = standardize_unit(txt_split[0])
            txt_split = txt_split[1:]
        else:
            unit_part = ''
        # print(unit_part, is_unit(unit_part))

        if number_part or unit_part:
            num_unit_part = '**'
            if number_part:
                num_unit_part = num_unit_part + number_part
            if unit_part:
                num_unit_part = num_unit_part + ' ' + unit_part
            num_unit_part = num_unit_part + '**'
            txt_split.insert(0, num_unit_part)

        # TODO: Check if second value is a unit

        # Combine string back together
        txt = '- ' + (' ').join(txt_split)
        txt = txt.replace(' - ', '\u2013')

        # PART 2: Find and format fractions (in both number part and text part)
        fraction_pattern = r'[1-9][0-9]*\/[1-9][0-9]*'
        txt = regex_replace(txt, fraction_pattern, make_fraction)
        # Remove space between non-fraction and fraction part of numbers
        test = r'\d &frac'
        txt = regex_replace(txt, test, lambda s: s.replace(' &frac', '&frac'))
    return txt


def regex_replace(string, regex_pattern, replace_func):
    """
    Take whatever pieces are found by a regex pattern and replace them with the
    output of `replace_func`
    """
    txt_re = re.findall(regex_pattern, string)
    txt_replacements = map(replace_func, txt_re)
    for orig, new in zip(txt_re, txt_replacements):
        string = string.replace(orig, new, 1)
    return string


def make_fraction(string):
    """
    Try to turn it into an HTML fraction, or just return the same string if that
    doesn't work
    """
    try:
        frac = Fraction(string)
        frac_str = '&frac{}{};'.format(frac.numerator, frac.denominator)
        return frac_str
    except ValueError:
        return string


def is_number(string):
    """
    Check if the input string is a number: integer (4), decimal (4.2), or fraction (1/4)
    For these purposes (looking for ranges) "-" or emdash also counts as a number
    :param val: String
    :return: Boolean (parseable to number)
    """
    try:
        # Integer or decimal
        float(string)
        return True
    except ValueError:
        # Fraction
        try:
            num, den = string.split('/')
            int(num)
            int(den)
            return True
        except ValueError:
            return False


# Starting to think about making units bold:
# make case-insensitive
# Ignore/remove "." if at end of unit

s_units = {
    ('teaspoon', 'teaspoons', 'tsp', 'tsps'): 'tsp',
    ('tablespoon', 'tablespoons', 'tbsp', 'tbsps'): 'Tbsp',
    ('mg', 'milligram', 'milligrams'): 'mg',
    ('g', 'gs', 'gram', 'grams'): 'g',
    ('kg', 'kgs', 'kilogram', 'kilograms', 'kilogramme', 'kilogrammes'): 'kg',
    ('ounce', 'ounces', 'oz', 'ozs'): 'oz',
    ('pound', 'pounds', 'lbs', 'lb', '#'): 'lb',
    ('liter', 'litre', 'L', 'l', 'liters', 'litres'): 'liter',
    ('q', 'qt', 'quart', 'qts', 'quarts'): 'quart',
    ('ml', 'milliliter', 'milliliters', 'millilitres', 'millilitre', 'cc'): 'ml',
}

units = [
    'cup', 'cups', 'stick', 'sticks', 'box', 'boxes', 'can', 'cans', 'bag',
    'bags', 'packet', 'packets', 'package', 'packages', 'pinch', 'pinches',
    'dash', 'dashes', 'drop', 'drops', 'scoop', 'scoops', 'slice', 'slices']


def clean_unit(unit):
    if len(unit) == 1:
        # Don't make lower case if it's a one-letter abbreviation
        return unit.rstrip('.')
    return unit.lower().rstrip('.')


def is_unit(string):
    """
    Check if the string is one of the unit options
    """
    str_clean = clean_unit(string)
    return str_clean in units or str_clean in [x for v in s_units.keys() for x in v]
    # return str_clean in units or str_clean in standard_units.keys()


def standardize_unit(unit):
    unit_clean = clean_unit(unit)
    if unit_clean in [x for v in s_units.keys() for x in v]:
        return [value for key, value in s_units.items() if unit_clean in key][0]
        # return s_units[unit_clean]
    else:
        return unit
