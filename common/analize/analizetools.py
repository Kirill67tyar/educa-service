from pprint import pprint
import sys
import builtins
from collections.abc import Mapping


# # for import
# from analizetools.analize import (
#     p_dir, p_mro, p_glob, p_loc, p_type,
#     delimiter, p_content, show_builtins,
#     show_doc, console, console_compose,
# )

# p_dir, p_mro, p_glob, p_loc, p_content, show_builtins, show_doc, delimiter

def p_dir(obj):
    return pprint(dir(obj))


def p_mro(obj):
    if isinstance(obj, type):
        return pprint(obj.mro())
    return pprint(type(obj).mro())


def p_glob():
    return pprint(globals())


def p_loc():
    return pprint(locals())


def p_content(obj):
    if hasattr(obj, '__iter__'):
        return pprint(obj)
    return pprint("Can't show elements of obj")


def show_builtins():
    # import builtins
    # pp(dir(builtins) == dir(globals()['__builtins__'])) # True
    # pp(builtins == globals()['__builtins__']) # True
    # pp(type(builtins)) # <class 'module'>
    # pp(type(builtins).mro()) # [<class 'module'>, <class 'object'>]
    key_builtins = globals().get('__builtins__')
    if key_builtins:
        if isinstance(key_builtins, dict):
            return pprint(key_builtins)
        return pprint(dir(key_builtins))
    else:
        return pprint("Can't show builtins")


def show_doc(obj):
    return print(obj.__doc__)


def delimiter(sym='-+', quant=50):
    return print('\n', sym * quant, end='\n')


def p_type(obj):
    return print(type(obj))


# потом можно улучшить чтобы передавался также **kwargs, и тогда выводился
# также имя переменной и её значенте
# поможет setattr
def console(*args, delimetr='- ', length=50, sdict=False):
    print('\n', '=' * 100)
    for elem in args:
        if issubclass(type(elem), (Mapping, dict)) or sdict:
            pprint(dict(elem))
        else:
            pprint(elem)
        print(delimetr * length)
    print('=' * 100, '\n')


def console_compose(
        obj,
        stype=True,
        smro=True,
        sdir=True,
        delimiter=delimiter,
        start=delimiter,
        end=delimiter
):
    params = (
        (stype, p_type, 'type:\n'),
        (smro, p_mro, 'mro:\n'),
        (sdir, p_dir, 'dir:\n'),

    )
    for action, func, view in params:
        if action:
            if params.index((action, func, view)) == 0:
                start()
            else:
                delimiter()
            print(view)
            func(obj)
    end()
