def makeReprStr(instance, spec=None):
    arg_list = []
    for field in spec or ():
        if isinstance(field, str):
            repr_name, attr_name = field, field
        else:
            repr_name, attr_name = field
        attr_val = getattr(instance, attr_name, 'N/A')
        arg_list.append('{}={}'.format(repr_name, attr_val))
    return '<{}({})>'.format(type(instance).__name__, ', '.join(arg_list))
