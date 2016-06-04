#import ipaddress

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

from core.models import num_to_ip
from ipdhcp.models import Dhcphosts_networks, Dhcphosts_hosts, User
from xbills import settings


def dhcps(request):
    print request.POST
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
    if 'edit_dhcp' in request.POST:
        edit_dhcp = Dhcphosts_networks.objects.get(id=request.POST['edit_dhcp'])
        print edit_dhcp
    return render(request, 'dhcp.html', locals())


def user_dhcp(request, uid):
    net_dhcp = Dhcphosts_networks.objects.all()
    user = User.objects.get(id=uid)
    host = Dhcphosts_hosts.objects.filter(uid=uid)
    if 'change' in request.GET:
        change_dhcp = Dhcphosts_hosts.objects.get(id=request.GET['change'])
    if 'dhcp_submit' in request.POST:
        try:
            ip_use = Dhcphosts_networks.objects.get(id=98)
            ip_host = Dhcphosts_hosts.objects.filter(network=98)
            #ip1 = int(ipaddress.IPv4Address(unicode(num_to_ip(ip_use.ip_range_first))))
            #ip2 = int(ipaddress.IPv4Address(unicode(num_to_ip(ip_use.ip_range_last))))
            #print ip2
            #count = ip2 - ip1
            # ip_use. = [1, 2, 3, 4, 5]
            # b = [5, 4, 3, 2, 1]
            #c = [num_to_ip(ip_host.ip)[i] for i in range(count) if num_to_ip(ip_host.ip)[i] != num_to_ip(ip_host.ip)[i]]
            #print c
        except:
            print 'no'
    return render(request, 'user_dhcp.html', locals())