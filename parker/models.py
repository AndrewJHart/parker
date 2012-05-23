""" TODO this should only be a temporary place to make sure the libary is built """

from django.conf import settings
from parker.library import parker_lib
from parker.util import smartimport

if getattr(settings, 'PARKER_AUTODISCOVER', True):
    for app in settings.INSTALLED_APPS:
        try:
            __import__(app + ".carriers")
        except ImportError:
            # TODO we probably need to be more specific than just import err
            # we only want to skip when the module doesn't exit
            pass
else:
    for carrier in settings.PARKER_CARRIERS:
        parker_lib.register(smartimport(carrier))
