Parker Settings
=====================

Parker makes use of some django settings.

PARKER_AUTODISCOVER
____________________
`default = True`
If this is True parker will import every installed apps carriers module when trying to populate it's registry.

PARKER_CARRIERS
________________
Carriers to register without autodiscover.

PARKER_TEMPLATES
_________________
Where parker should search for mustache templates.

PARKER_DEFAUlT_SOCKET
_____________________
Where the widgets should connect to browsermq.

PARKER_BROKER_URL
____________________
Where parker should publish too. Needs some work.


