import logging
from django.http import HttpResponseServerError
from django.utils.translation import gettext as _

from utils.telegram import report_to_admin


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            # Log the exception
            logging.exception(str(e))
            report_to_admin(
                f"Exception occurred: {request.path} \n\n"
                f"Exception occurred while processing {request.path}:\n{str(e)}"
            )
            # Return a custom error page
            response = HttpResponseServerError(
                _(
                    "Oops! Something went wrong. "
                    "Contact us to solve the issue if it is important."
                )
            )
        return response
