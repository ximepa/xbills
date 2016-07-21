# -*- encoding: utf-8 -*-
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from .models import Claims, Queue, Comments, ClaimState, Priority, Log, Workers
from core.models import Admin as User
# from .forms import ClaimsCreateForm, CommentAddForm, StateAddForm, PriorityAddForm, QueueAddForm, UserSettingsForm
from django.conf import settings
from django.db.models import Count
from django.contrib.auth import logout
from django.db.models import Q
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from pygeocoder import Geocoder
from geopy.geocoders import Nominatim


@login_required(login_url='/login/')
@csrf_exempt
def abills_claims_add(request):
    if request.method == 'POST':
        print request.POST
        if request.POST['flat'] != '':
            flat = u' кв.' + request.POST['flat']
            claims = Claims(address=request.POST['district'] + ' ' + request.POST['street'] + ' ' + request.POST['build'] + flat,
                      uid=request.POST['uid'], email=request.POST['email'], queue_id=request.POST['queue'],
                      owner_id = request.user.pk, problem=request.POST['problem']
            )
        else:
            claims = Claims(address=request.POST['district'] + ' ' + request.POST['street'] + ' ' + request.POST['build'],
                      uid=request.POST['uid'], email=request.POST['email'], queue_id=request.POST['queue'],
                      owner_id = request.user.pk, problem=request.POST['problem']
            )
        print claims
        claims.save()
    response = HttpResponse()
    return redirect(reverse('claims:list'))


@login_required(login_url='/login/')
def name(request):
    if request.method == 'POST':
        u = User.objects.get(pk=request.user.pk)
        u.first_name = request.POST['firstname']
        u.last_name = request.POST['lastname']
        u.save()
    else:
        print 'asd'
    return redirect('dashboard')


def index(request):
    if 'claim_notifi' in request.GET:
        claim = Claims.objects.filter(state=1).last()
        pay_list = {}
        pay_list['claim'] = claim.problem, claim.uid, claim.owner.login, claim.queue.name, claim.address
        res_json = json.dumps(pay_list)
        return HttpResponse(res_json)
    queue = Queue.objects.all()
    claims_list_opened = Claims.objects.filter(state=1).count()
    claims_list_closed = Claims.objects.filter(state=2).count()
    list = []
    list1 = []
    for q in queue:
        list.append({'name': q.name, 'opened': q.claims.filter(state=1).count(), 'closed': q.claims.filter(state=2).count(), 'all': q.claims.all().count()})
    list1.append({'all_opened': claims_list_opened, 'all_closed': claims_list_closed})
    users = User.objects.all()
    return render(request, 'claims.html', locals())


def logout_view(request):
    logout(request)
    return redirect(reverse('dashboard'))


@login_required(login_url='/login/')
def claims_list(request, template_name='claims/claims_list.html'):
    order_by = request.GET.get('order_by', 'created')
    print request.GET
    qu = Queue.objects.get(pk=1)
    filter_by = request.GET.get('filter_by', qu.id)
    claims = Claims.objects.filter(state=1, queue_id=filter_by).order_by('-priority', order_by)
    claims_count = Queue.objects.filter(claims__state=1).order_by('id').values('name', 'id').annotate(Count('claims'))
    user_claims_count = Queue.objects.filter(claims__queue=1, claims__state=1).values('name', 'id').annotate(Count('claims'))
    if request.method == 'GET' and 'search' in request.GET:
        if request.GET['search'] != '':
            claims = Claims.objects.filter(Q(state=1), Q(address__icontains=request.GET['search']) |
                Q(login__icontains=request.GET['search']) | Q(owner__username__icontains=request.GET['search']) |
                Q(problem__icontains=request.GET['search']) | Q(uid__icontains=request.GET['search']))
    paginator = Paginator(claims, 20)
    page = request.GET.get('page')

    return render(request, 'claims_list.html', locals())

@login_required(login_url='/login/')
def claims_list_all(request, template_name='claims/claims_list.html'):
    order_by = request.GET.get('order_by', '-created')
    user_bills_url = settings.USER_BILLS_URL
    qu = Queue.objects.get(pk=1)
    filter_by = request.GET.get('filter_by', qu.id)
    cur_queue = Queue.objects.get(pk=filter_by)
    claims = Claims.objects.filter(queue_id=filter_by).order_by(order_by)
    claims_count = Queue.objects.order_by('id').values('name', 'id').annotate(Count('claims'))
    user_claims_count = Queue.objects.filter(claims__queue=request.user.queue).values('name', 'id').annotate(Count('claims'))
    if request.method == 'GET' and 'search' in request.GET:
        if request.GET['search'] != '':
            claims = Claims.objects.filter(Q(address__icontains=request.GET['search']) |
                Q(login__icontains=request.GET['search']) | Q(owner__username__icontains=request.GET['search']) |
                Q(problem__icontains=request.GET['search']) | Q(uid__icontains=request.GET['search']))
    paginator = Paginator(claims, request.user.claims_per_page)
    page = request.GET.get('page')
    try:
        claims_list = paginator.page(page)
    except PageNotAnInteger:
        claims_list = paginator.page(1)
    except EmptyPage:
        claims_list = paginator.page(paginator.num_pages)
    return render(request, template_name, {
        'claims': claims_list,
        'claims_count': claims_count,
        'user_claims_count': user_claims_count,
        'user_bills_url': user_bills_url,
        'cur_queue': cur_queue,

    })

# @login_required(login_url='/login/')
# def claim_create(request, template_name='claims/claim_create_form.html'):
#     if request.user.has_perm('claims.add_claims'):
#         form = ClaimsCreateForm()
#         if request.method == 'POST':
#             form = ClaimsCreateForm(request.POST)
#             if form.is_valid():
#                 vehicle = form.save(commit=False)
#                 vehicle.owner_id = request.user.id
#                 vehicle.save()
#                 if request.POST['comments'] != '':
#                     comments = Comments(user_id=request.user.pk, claim_id=vehicle.pk, comments=request.POST['comments'], title=request.POST['problem'])
#                     comments.save()
#                 return redirect(reverse('claims:list'))
#             else:
#                 print 'form not valid'
#         else:
#             print 'no post'
#         return render(request, template_name, {'form': form})
#     else:
#         return render(request, 'errors/404.html')

# @login_required(login_url='/login/')
# def claim_edit(request, id):
#     claim = get_object_or_404(Claims, pk=id)
#     priority = Priority.objects.all()
#     queue = Queue.objects.all()
#     comments = Comments.objects.filter(claim_id=claim.pk)
#     comment_form = CommentAddForm()
#     queue_form = QueueAddForm(initial={'queue': claim.queue})
#     state_form = StateAddForm(initial={'worker': claim.worker, 'state': claim.state})
#     priority_form = PriorityAddForm(initial={'priority': claim.priority})
#     if request.method == 'POST':
#         if 'create_comment' in request.POST:
#             comment_form = CommentAddForm(request.POST)
#             if comment_form.is_valid():
#                 vehicle = comment_form.save(commit=False)
#                 vehicle.user_id = request.user.id
#                 vehicle.claim_id = claim.pk
#                 log = Log(user_id=request.user.pk, claim_id=id, action='Added comment')
#                 log.save()
#                 vehicle.save()
#                 return redirect(request.get_full_path())
#             else:
#                 print 'form not valid'
#         if 'change_state' in request.POST:
#             state_form = StateAddForm(request.POST)
#             if state_form.is_valid():
#                 try:
#                     worker = int(request.POST['worker'])
#                 except:
#                     worker = None
#                 if worker != None:
#                     action = ''
#                     if claim.worker_id != worker:
#                         action = action + 'Worker changed (%s to %s)' % (claim.worker, Workers.objects.get(pk=worker))
#                     if claim.state_id != int(request.POST['state']):
#                         if action == '':
#                             action = action + 'State changed (%s to %s)' % (claim.state, ClaimState.objects.get(pk=request.POST['state']))
#                         else:
#                             action = action + ' | State changed (%s to %s)' % (claim.state, ClaimState.objects.get(pk=request.POST['state']))
#                     log = Log(user_id=request.user.pk, claim_id=id, action=action)
#                     log.save()
#                 else:
#                     if claim.worker_id == worker:
#                         log = Log(user_id=request.user.pk, claim_id=id, action='Nothing changed')
#                     else:
#                         log = Log(user_id=request.user.pk, claim_id=id, action='Worker changed (%s to None)' % claim.worker)
#                     log.save()
#                 if request.POST['comments']:
#                     comments = Comments(user_id=request.user.id, claim_id=id, comments=request.POST['comments'])
#                     comments.save()
#                 claim.worker_id = request.POST['worker']
#                 claim.state_id = request.POST['state']
#                 claim.save()
#                 return redirect(request.get_full_path())
#             else:
#                 print 'form not valid'
#         if 'change_priority' in request.POST:
#             priority_form = PriorityAddForm(request.POST)
#             if priority_form.is_valid():
#                 log = Log(user_id=request.user.pk, claim_id=id, action='Priority changed (%s to %s)' % (claim.priority, Priority.objects.get(pk=request.POST['priority'])))
#                 if request.POST['comments']:
#                     comments = Comments(user_id=request.user.id, claim_id=id, comments=request.POST['comments'])
#                     comments.save()
#                 claim.priority_id = request.POST['priority']
#                 log.save()
#                 claim.save()
#                 return redirect(request.get_full_path())
#             else:
#                 print 'form not valid'
#         if 'change_queue' in request.POST:
#             queue_form = QueueAddForm(request.POST)
#             print request.POST
#             if queue_form.is_valid():
#                 log = Log(user_id=request.user.pk, claim_id=id, action='Queue changed (%s to %s)' % (claim.queue, Queue.objects.get(pk=request.POST['queue'])))
#                 comments = Comments(user_id=request.user.id, claim_id=id, comments=request.POST['comments'])
#                 claim.queue_id = request.POST['queue']
#                 log.save()
#                 comments.save()
#                 claim.save()
#                 return redirect(request.get_full_path())
#             else:
#                 print 'form not valid'
#     return render(request, 'claim_edit_form.html', {
#         'priority': priority,
#         'claim': claim,
#         'pk': id,
#         'comments': comments,
#         'comment_form': comment_form,
#         'queue_form': queue_form,
#         'state_form': state_form,
#         'priority_form': priority_form,
#         'user_bills_url': '/',
#         'queue': queue,
#     })

# @login_required(login_url='/login/')
# def claim_comment_add(request, pk, template_name='claims/claim_comment_add.html'):
#     claim = get_object_or_404(Claims, pk=pk)
#     comments = Comments.objects.filter(claim_id=claim.pk)
#     form = CommentAddForm()
#     if request.method == 'POST':
#         form = CommentAddForm(request.POST)
#         if form.is_valid():
#             comments = form.save(commit=False)
#             comments.user_id = request.user.id
#             comments.save()
#             return redirect(reverse('claims:list'))
#         else:
#             print 'form not valid'
#     else:
#         print 'no post'
#     return render(request, template_name, {'form': form, 'claim': claim, 'comments': comments})

@login_required(login_url='/login/')
def claim_delete(request, pk, template_name='claims/claim_confirm_delete.html'):
    claim = get_object_or_404(Claims, pk=pk)
    if request.method == 'POST':
        claim.delete()
        return redirect(reverse('claims:list'))
    return render(request, template_name, {'claim': claim})


def claim_map(request, claim_id):
    claim = Claims.objects.get(pk=claim_id)
    address = claim.address
    try:
        geolocator = Nominatim()
        location = geolocator.geocode(address.encode('utf-8') + ", Умань, Україна")
        lat = location.latitude
        str_lat = str(lat)
        min_lat = str(lat - 0.0008)
        max_lat = str(lat + 0.0008)
        lon = location.longitude
        str_lon = str(lon)
        min_lon = str(lon - 0.00117)
        max_lon = str(lon + 0.00117)
    except:
        results = Geocoder.geocode(address.encode('utf-8') + ", Умань, Україна")
        lat = results[0].coordinates[0]
        str_lat = str(lat)
        min_lat = str(lat - 0.0008)
        max_lat = str(lat + 0.0008)
        lon = results[0].coordinates[1]
        str_lon = str(lon)
        min_lon = str(lon - 0.00117)
        max_lon = str(lon + 0.00117)
    return render(request, 'maps.html', locals())


# @login_required(login_url='/login/')
# def user_settings(request, template_name='user/settings.html'):
#     settings_form = UserSettingsForm(initial={
#         'claims_per_page': request.user.claims_per_page,
#         'comments_per_page': request.user.comments_per_page,
#         'logs_per_page': request.user.logs_per_page,
#         'queue': request.user.queue,
#         'email': request.user.email,
#     })
#     user = User.objects.get(pk=request.user.pk)
#     if request.method == 'POST':
#         print request.POST
#         settings_form = UserSettingsForm(request.POST)
#         if settings_form.is_valid():
#             user.claims_per_page = request.POST['claims_per_page']
#             user.comments_per_page = request.POST['comments_per_page']
#             user.logs_per_page = request.POST['logs_per_page']
#             user.queue_id = request.POST['queue']
#             user.email = request.POST['email']
#             user.save()
#             return redirect(reverse('user_settings'))
#     return render(request, template_name, {
#         'settings_form': settings_form,
#     })

