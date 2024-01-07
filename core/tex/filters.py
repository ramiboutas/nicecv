""""  This code is a copy from https://github.com/weinbusch/django-tex """

import re

from django.template.defaultfilters import register


REPLACEMENTS = dict(
    [
        ("&", "\\&"),
        ("%", "\\%"),
        ("$", "\\$"),
        ("#", "\\#"),
        ("_", "\\_"),
        ("{", "\\{"),
        ("}", "\\}"),
        ("\\", "\\textbackslash{}"),
        ("~", "\\textasciitilde{}"),
        ("^", "\\textasciicircum{}"),
    ]
)

ESCAPE_PATTERN = re.compile("[{}]".format("".join(map(re.escape, REPLACEMENTS.keys()))))


def do_latex_escape(value: object) -> str:
    """
    Replace all LaTeX characters that could cause the latex compiler to fail
    and at the same time try to display the character as intended from the user.

    see also https://tex.stackexchange.com/questions/34580/escape-character-in-latex
    """
    value = str(value)
    return ESCAPE_PATTERN.sub(lambda mo: REPLACEMENTS.get(mo.group()), value)


def do_linebreaks(value: str) -> str:
    return value.replace("\n", "\\\\\n")


tex_specific_filters = {
    "latex_escape": do_latex_escape,
    "linebreaks": do_linebreaks,
}

FILTERS = register.filters.copy()
FILTERS.update(tex_specific_filters)
