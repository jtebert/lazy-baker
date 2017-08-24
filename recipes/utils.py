def format_ingredient_line(txt):
    '''
    Formats a single line of an ingredients list into Markdown for putting on the page
    :param txt: String line of text
    :return: Text in markdown form (to be turned into HTML by make_markdown)
    '''

    txt_split = txt.split()
    first_is_number = False
    second_is_unit = False
    if len(txt_split) == 0:
        # This is a blank line
        pass
    elif len(txt) >= 2 and txt[0] == '[' and txt[-1] ==']':
        # This is a section marker
        txt = '### ' + txt[1:-1]
    else:
        # This is an ingredient line
        # Check if first value is a number (will get decimals, fractions, and integers)
        try:
            float(txt[0])
            first_is_number = True
        except ValueError:
            pass
        # Check if first value is a number range (e.g., 6-8)
        range_split = txt[0].split('-')
        if len(range_split) == 3:
            try:
                float(range_split[0])
                float(range_split[2])
                first_is_number = True
            except:
                pass
        # Make number bold
        if first_is_number:
            txt_split[0] = '**' + txt_split[0] + '**'
        # TODO: Check if second value is a unit

        # Combine string back together
        txt = '- ' + (' ').join(txt_split)
    return txt