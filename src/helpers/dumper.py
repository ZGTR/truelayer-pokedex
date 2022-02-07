from cytoolz import valfilter


def json_dumper(obj):
    try:
        return obj.toJSON()
    except:
        try:
            return obj.__dict__
        except:
            return dir(obj)


def filter_none(d):
    return valfilter(lambda v: v not in [None, {}, '', []], d)
