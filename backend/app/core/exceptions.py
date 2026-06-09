class NotFoundError(Exception):
    def __init__(self, resource: str, identifier: str):
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} '{identifier}' not found")


class AppValidationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
