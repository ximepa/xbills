from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def type_f_list(list, db):
    result = []
    for value in list.keys():
        if value in db:
            result.append(list[value])
    return result

def db_filter(db):
    print tuple(eval(db))


def pagins(model, request):
    page_list = None
    out_sum = 0.0
    paginator = Paginator(model, 20)
    page = request.GET.get('page', 1)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)
    if int(page) > 5:
        start = str(int(page)-5)
    else:
        start = 1
    if int(page) < paginator.num_pages-5:
        end = str(int(page)+3)
    else:
        end = paginator.num_pages+1
    page_range = range(int(start), int(end)),
    for p in page_range:
        page_list = p
    pre_end = items.paginator.num_pages - 2
    try:
        for sum in items:
            out_sum += sum.sum
    except:
        pass
    return {'page': page, 'items': items, 'start': start, 'end': end, 'pre_end': pre_end, 'page_list': page_list, 'out_sum': out_sum}
