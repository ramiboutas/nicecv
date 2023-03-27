from django.apps import apps


def get_child_models(app_label: str, AbstractClass):
    if app_label not in [app.label for app in apps.get_app_configs()]:
        raise Exception(f"{app_label} is not installed in the project")

    result = []
    for model in apps.get_app_config(app_label).get_models():
        if issubclass(model, AbstractClass) and model is not AbstractClass:
            result.append(model)
    return result
