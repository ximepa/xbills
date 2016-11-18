import json
import random
import csv
from django.conf import settings
import os
from django.shortcuts import HttpResponse
from .models import Admin
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.core.cache import cache
from django.core import serializers
from django.shortcuts import render


def randomDigits(digits):
    lower = 10**(digits-1)
    upper = 10**digits - 1
    return random.randint(lower, upper)


def module_check(module):
    modules = settings.INSTALLED_APPS
    module_path = os.path.join(settings.BASE_DIR,  module)
    if module in modules and os.path.exists(module_path):
        return True
    else:
        return False


def export_to_csv(request, queryset, fields, name):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename=%s.csv' % name
    # opts = queryset.model._meta
    # field_names = [field.name for field in opts.fields]
    writer = csv.writer(response)
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in fields])
    return response


def export_to_xml(request, queryset):
    xml_data = serializers.serialize("xml", queryset)
    print xml_data
    return render(request, 'base.xml', {'data': xml_data}, content_type="text/xml")


def get_online():
    ids = cache.get('online-now')
    return Admin.objects.filter(id__in=ids)


def api_search(model, request):
    list = []
    for item in model.objects.filter(id=request.GET[request.GET['method']]):
        dict_resp = {}
        dict_resp['value'] = str(item.id)
        dict_resp['name'] = item.name
        list.append(dict_resp)
    dict_out = {"success": "true", "results": list}
    jsonFormat = json.dumps(dict_out)
    return jsonFormat


def get_all_fields(model):
    """Returns a list of all field names on the instance."""
    fields = []
    for f in model._meta.fields:

        fname = f.name
        # resolve picklists/choices, with get_xyz_display() function
        get_choice = 'get_'+fname+'_display'
        if hasattr(model, get_choice):
            value = getattr(model, get_choice)()
            print 'hasattr'
            print value
            print '====='
        else:
            try :
                value = getattr(model, fname)
                print 'getattr'
                print value
                print '========'
            except AttributeError:
                value = None

        # only display fields with values and skip some fields entirely
        if f.editable and value and f.name not in ('id', 'status', 'workshop', 'user', 'complete') :

            fields.append(
              {
               'label':f.verbose_name,
               'name':f.name,
               'value':value,
              }
            )
    return fields