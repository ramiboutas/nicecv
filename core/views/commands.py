import subprocess

from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from django.http import Http404
from django.http import HttpResponse


@login_required
def run(request, args):
    if request.user.is_superuser:
        # call_command(args)
        subprocess.call("touch file_created_from_url.txt", shell=True)
        subprocess.call(
            "source venv/bin/activate && python manage.py" + args, shell=True
        )

        return HttpResponse("Command run!")
    raise Http404()
