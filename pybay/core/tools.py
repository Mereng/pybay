def strbool(str):
    if str in ('true', 'True'):
        return True
    elif str in ('False', 'false'):
        return False
    return None


def limit_offset(data, max_limit):
    limit = max_limit
    offset = 0
    if 'limit' in data:
        try:
            limit = min(int(data['limit']), max_limit)
        except ValueError:
            pass

    if 'offset' in data:
        try:
            offset = max(int(data['offset']), 0)
        except ValueError:
            pass
    return limit, offset
