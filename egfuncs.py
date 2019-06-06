def iterable(obj):
    if type(obj) == 'str':
        return False
    try:
        iter(obj)
        return True
    except TypeError:
        return False
