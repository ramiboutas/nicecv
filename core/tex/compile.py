import tempfile
from pathlib import Path
from subprocess import CalledProcessError
from subprocess import PIPE
from subprocess import run

from django.conf import settings
from django.template.loader import get_template

from ..exceptions import TexError


def compile_template_to_pdf(tex, context):
    template = get_template(tex.template_name, using="tex")
    source = template.render(context)
    with tempfile.TemporaryDirectory() as tempdir:
        temppath = Path(tempdir)
        filename = "texput.tex"
        with open(temppath / filename, "x", encoding="utf-8") as f:
            f.write(source)
        args = f"{tex.interpreter} -interaction=batchmode {tex.interpreter_options} {filename} 2>&1 > /dev/null"
        try:
            run(args, shell=True, stdout=PIPE, stderr=PIPE, check=True, cwd=tempdir)
        except CalledProcessError as called_process_error:
            try:
                with open(temppath / "texput.log", encoding="utf-8") as f:
                    log = f.read()
            except FileNotFoundError:
                raise called_process_error
            else:
                raise TexError(log=log, source=source, template_name=tex.template_name)
        with open(temppath / "texput.pdf", "rb") as f:
            pdf = f.read()
        return pdf
