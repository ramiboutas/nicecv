from django_tex.environment import environment

def hhmm_format(value):
    pass # as above

def my_environment(**options):
    env = environment(**options)
    env.filters.update({
        'hhmm_format': hhmm_format
    })
    return env
