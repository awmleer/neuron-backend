from django.http import JsonResponse

class ErrorResponse(JsonResponse):
    def __init__(self, message, payload=None):
        super().__init__({
            'message': message,
            'payload': payload
        })
        self.status_code = 444

