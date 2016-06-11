#import ipaddress

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from core.models import num_to_ip, ip_to_num
from .models import Dhcphosts_networks, Dhcphosts_hosts, User, ipRange
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
    ip_list_db = []
    net_dhcp = Dhcphosts_networks.objects.all()
    user = User.objects.get(id=uid)
    host = Dhcphosts_hosts.objects.filter(uid=uid)
    # if 'change' in request.GET:
    #     change_dhcp = Dhcphosts_hosts.objects.get(id=request.GET['change'])
    if 'dhcp_submit' in request.POST:
        print request.POST
        change_dhcp = Dhcphosts_hosts.objects.get(id=request.POST['uid'])
        try:
            if 'auto_select' in request.POST:
                ip_db_range = net_dhcp.get(id=int(request.POST['networks']))
                ip_db = Dhcphosts_hosts.objects.filter(network=int(request.POST['networks']))
                ip_range = ipRange(num_to_ip(ip_db_range.ip_range_first), num_to_ip(ip_db_range.ip_range_last))
                for db_ip in ip_db:
                    ip_list_db.append(num_to_ip(db_ip.ip))
                result_ip = [i for i in ip_range if i not in ip_list_db]
            get_ip = result_ip[0]
            change_dhcp.uid = request.POST['uid']
            if request.POST['ip'] != None:
                change_dhcp.ip = ip_to_num(request.POST['ip'])
            else:
                change_dhcp.ip = ip_to_num(get_ip)
            change_dhcp.hostname = request.POST['hostname']
            change_dhcp.mac = request.POST['mac']
            change_dhcp.network = request.POST['networks']
            # change_dhcp.save()
        except:
            print 'no'
    return render(request, 'user_dhcp.html', locals())