""" TODO this should only be a temporary place to make sure the libary is built """

from django.conf import settings
from parker import parker_lib
from parker.util import load_carrier

for carrier in settings.PARKER_CARRIERS:
    parker_lib[carrier] = load_carrier(carrier)
