""" TODO this should only be a temporary place to make sure the libary is built """

from django.conf import settings
from parker.library import parker_lib
from parker.util import smartimport

for carrier in settings.PARKER_CARRIERS:
    parker_lib.register(smartimport(carrier))
