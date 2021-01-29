from datetime import date


def fill_spaces(txtval: str, size: int) -> str:
    """fill with spaces from the right side of txtval"""
    if txtval == '' or txtval is None:
        return ' ' * size
    len_txtval = len(txtval)
    if len_txtval > size:
        raise ValueError('Value is bigger than size')
    return txtval + ' ' * (size - len_txtval)


def fill_spaces_cut(txtval: str, size: int) -> str:
    """fill with spaces from the right side of txtval.
        If len(txtval) > size then returns txtval[:size]
    """
    return fill_spaces(txtval[:size], size)


def decimal2flat(number, size):
    """
    Transforms a number 123.456,78 to string 00012345678
    """
    txtval = f'{round(number, 2)}'.replace(',', '').replace('.', '')
    len_txtval = len(txtval)
    if len_txtval > size:
        raise ValueError('Value is bigger than size')
    return '0' * (size - len_txtval) + txtval


def leading_zeroes(val, size):
    """Tranforms an integer 123456 to 000123456"""
    txtval = str(val)
    len_txtval = len(txtval)
    if len_txtval > size:
        raise ValueError('Value is bigger than size')
    return '0' * (size - len_txtval) + txtval


def isodate2flat(isodate):
    """
    Transforms an isodate yyyy-mm-dd to text ddmmyyyy
    """
    if isodate == '' or isodate is None:
        return ' ' * 8
    isodate_type = type(isodate)
    if isodate_type == date:
        isodate = isodate.isoformat()
    elif isodate_type == str:
        pass
    else:
        raise ValueError(f'{isodate} is not of proper type')
    yyyy, mm, dd = isodate.split('-')
    return f'{dd}{mm}{yyyy}'
