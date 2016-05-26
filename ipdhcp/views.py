from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from ipdhcp.models import Dhcphosts_networks, Dhcphosts_hosts, User
from xbills import settings


def dhcps(request):
    order_by = request.GET.get('order_by', 'id')
    net_dhcp = Dhcphosts_networks.objects.all().order_by(order_by)
    paginator = Paginator(net_dhcp, settings.FEES_PER_PAGE)
    page = request.GET.get('page', 1)
    try:
        dhcp_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        dhcp_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        dhcp_page = paginator.page(paginator.num_pages)
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
    pre_end = dhcp_page.paginator.num_pages - 2
    return render(request, 'dhcp.html', locals())

def user_dhcp(request, uid):
    user = User.objects.get(id=uid)
    host = Dhcphosts_hosts.objects.filter(uid=uid)
    print host.values()
    return render(request, 'user_dhcp.html', locals())