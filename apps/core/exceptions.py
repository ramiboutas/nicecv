class BaseException(Exception):
    pass


class FormException(BaseException):
    pass


class ErrorBySettingFormFieldAttributes(FormException):
    pass


class ErrorBySettingFormWidgetInputType(FormException):
    pass
