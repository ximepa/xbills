


def type_f_list(list, db):
    result = []
    for value in list.keys():
        if value in db:
            result.append(list[value])
    return result

def db_filter(db):
    print tuple(eval(db))