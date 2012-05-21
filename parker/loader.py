""" this is a kind of django like template loader
it's like this so we can render starter content into the divs if we want at some point
django-mustachejs doesn't look right for this since I don't want to stick them into the global namespace
"""
from django.conf import settings
from django.template.base import TemplateDoesNotExist
from django.utils._os import safe_join


class ParkerLoader(object):
    """ this is basically just the filesystem loader from django except it can't compile
    """
    is_usable = True
    def __init__(self):
        pass

    def load_template_source(self, template_name, template_dirs=None):
        """ this is basically just the filesystem loader from django """
        tried = []
        for filepath in self.get_template_sources(template_name, template_dirs):
            try:
                file = open(filepath)
                try:
                    return (file.read().decode(settings.FILE_CHARSET), filepath)
                finally:
                    file.close()
            except IOError:
                tried.append(filepath)
        if tried:
            error_msg = "Tried %s" % tried
        else:
            error_msg = "Your TEMPLATE_DIRS setting is empty. Change it to point to at least one template directory."
        raise TemplateDoesNotExist(error_msg)


    def get_template_sources(self, template_name, template_dirs=None):
        """ returns absolute paths to the possible locations for template_name
            more or less copied from django.templates.loaders.filesystem
        """
        if not template_dirs:
            template_dirs = settings.PARKER_TEMPLATE_DIRS

        for tdir in template_dirs:
            # these are the things django worries about so I will copy them
            try:
                yield safe_join(tdir, template_name)
            except ValueError:
                # according to django.templates.loaders.filesystem this isn't fatal
                pass

