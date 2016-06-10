from django.shortcuts import render
from .models import Client
from .forms import ClientAddForm, ClientChangeForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def index(request):
    return render(request, 'index.html', locals())


def clients(request):
    clients_list = Client.objects.all()
    if 'uid' in request.GET:
        user = Client.objects.get(pk=request.GET['uid'])
        form = ClientChangeForm(instance=user)
    if 'command' in request.GET:
        if request.GET['command'] == 'add_form':
            add = request.GET['command']
            form = ClientAddForm()
            if request.method == 'POST':
                print request.POST
                form = ClientAddForm(request.POST)
                if form.is_valid:
                    form.save()
    paginator = Paginator(clients_list, 100)
    page = request.GET.get('page', 1)
    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        clients = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        clients = paginator.page(paginator.num_pages)
    if int(page) > 5:
        start = str(int(page)-5)
    else:
        start = 1
    if int(page) < paginator.num_pages-5:
        end = str(int(page)+5+1)
    else:
        end = paginator.num_pages+1
    page_range = range(int(start), int(end)),
    for p in page_range:
        page_list = p
    pre_end = clients.paginator.num_pages - 2
    return render(request, 'clients.html', locals())