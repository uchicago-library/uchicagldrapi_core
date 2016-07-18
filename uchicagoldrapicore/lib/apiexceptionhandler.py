class APIExceptionHandler(object):
    def __init__(self):
        pass

    def handle(self, e):
        # Placeholder
        if not isinstance(e, Exception):
            raise ValueError("The exception handler only handles exceptions.")
        return {"Exception": str(e)}
