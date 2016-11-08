


def type_f_list(list, db):
    result = []
    for key, value in list:
        print key, value
        if key in db:
            result.append(value)
    return tuple(result)
