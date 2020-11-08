import re


def test_pattern(pattern, value):
    result = []
    m = re.match(pattern, value)

    if m:
        result.append('match')
        if m.groupdict():
            result.extend(['{}: {}'.format(k, v) for k, v in m.groupdict().items()])
    else:
        result.append('no match')

    return '\n'.join(result)


def get_group(m, group_name):
    try:
        return m.group(group_name)
    except IndexError:
        return None
