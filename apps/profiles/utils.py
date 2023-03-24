import inspect


from . import models as profile_module

from .models import AbstractChild


def get_profile_children():
    class_objs = [
        cls_obj
        for _, cls_obj in inspect.getmembers(profile_module)
        if inspect.isclass(cls_obj) and AbstractChild in cls_obj.__bases__
    ]
    return class_objs
