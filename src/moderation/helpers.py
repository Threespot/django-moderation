from moderation.register import RegistrationError


def automoderate(instance, user):
    '''
    Auto moderates given model instance on user. Returns moderation status:
    0 - Rejected
    1 - Approved
    '''
    try:
        status = instance.moderated_object.automoderate(user)
    except AttributeError:
        msg = u"%s has been registered with Moderation." % instance.__class__
        raise RegistrationError(msg)

    return status


def import_moderator(app):
    '''
    Import moderator module and register all models it contains with moderation
    '''
    from django.utils.importlib import import_module
    import imp
    import sys

    try:
        app_path = import_module(app).__path__
    except AttributeError:
        return None

    try:
        imp.find_module('moderator', app_path)
    except ImportError:
        return None
    
    module = import_module("%s.moderator" % app)
    
    return module


def import_project():
    '''
    Import moderator from project root and register all models it contains with
    moderation. The project root file allows you to add moderation for models
    that are in libraries outside the project.
    '''
    from django.conf import settings
    from django.utils.importlib import import_module
    import imp
    import sys
    
    project_root = settings.ROOT_URLCONF.split(".")[0]
    
    try:
        app_path = import_module(project_root).__path__
    except AttributeError:
        return None

    try:
        imp.find_module('moderator', app_path)
    except ImportError:
        return None
    
    module = import_module("%s.moderator" % project_root)
    
    return module    
    
def auto_discover():
    '''
    Auto register all apps that have module moderator with moderation
    '''
    from django.conf import settings
    
    for app in settings.INSTALLED_APPS:
        import_moderator(app)
    
    import_project()
    