import re


def test_pattern(pattern, value):
    result = {'match': False,
              'groups': {}}
    m = re.match(pattern, value)

    if m:
        result['match'] = True
        if m.groupdict():
            result['groups'] = {k: v for k, v in m.groupdict().items()}

    return result


def get_group(m, group_name):
    try:
        return m.group(group_name)
    except IndexError:
        return None
