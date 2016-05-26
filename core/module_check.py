from django.conf import settings
import os


def check(module):
    modules = settings.INSTALLED_APPS
    module_path = os.path.join(settings.BASE_DIR,  module)
    if module in modules and os.path.exists(module_path):
        return True
    else:
        return False