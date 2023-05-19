""" This module will be used to make some performance checks """

import inspect
from time import time
from functools import cache

from django.apps import apps

from apps.profiles import models


@cache
def get_models_with_cache():
    return apps.get_app_config("profiles").get_models()


def get_models_without_cache():
    return apps.get_app_config("profiles").get_models()


def access_model_name_using__meta(Models):
    out = []
    for Model in Models:
        out.append(Model._meta.model_name)


def access_class_name(Models):
    out = []
    for Model in Models:
        out.append(Model.__name__)


def perfom():
    # get models with cache
    get_models_cache_start = time()
    Models = get_models_with_cache()
    print(
        "# Get models using cache: %s microseconds"
        % (1e6 * (time() - get_models_cache_start))
    )
    # get models without cache
    get_models_without_cache_start = time()
    get_models_without_cache()
    print(
        "# Get models without cache: %s microseconds"
        % (1e6 * (time() - get_models_without_cache_start))
    )

    # Model._meta.model_name
    models_meta_start = time()
    access_model_name_using__meta(Models)

    print(
        "# Model._meta.model_name: %s microseconds"
        % (1e6 * (time() - models_meta_start))
    )
    # Model.__name__
    class_name_start = time()
    access_class_name(Models)
    print("# Model.__name__: %s microseconds" % (1e6 * (time() - class_name_start)))
