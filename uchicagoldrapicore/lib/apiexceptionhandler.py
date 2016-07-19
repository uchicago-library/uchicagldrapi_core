from ..responses.apiresponse import APIResponse

class APIExceptionHandler(object):
    def __init__(self):
        pass

    def handle(self, e):
        # Placeholder
        if not isinstance(e, Exception):
            raise ValueError("The exception handler only handles exceptions.")
        fail_str = "({}): {}".format(str(type(e)), str(e))
        return APIResponse("fail",
                           errors = [fail_str])
