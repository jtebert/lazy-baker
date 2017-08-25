import re

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
    elif len(txt) >= 2 and txt[0] == '[' and txt[-1] ==']':
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

        if number_part:
            number_part = re.sub(' - ', ur'\u2013', number_part)
            number_part = '***' + number_part + '***'
        txt_split.insert(0, number_part)

        # TODO: Check if second value is a unit

        # Combine string back together
        txt = '- ' + (' ').join(txt_split)
    return txt

def is_number(str):
    """
    Check if the input string is a number: integer (4), decimal (4.2), or fraction (1/4)
    For these purposes (looking for ranges) "-" or emdash also counts as a number
    :param val: String
    :return: Boolean (parseable to number)
    """
    try:
        # Integer or decimal
        float(str)
        return True
    except ValueError:
        # Fraction
        try:
            num, den = str.split('/')
            int(num)
            int(den)
            return True
        except ValueError:
            return False
