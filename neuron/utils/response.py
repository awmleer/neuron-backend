from django.http import JsonResponse

class ErrorResponse(JsonResponse):
    def __init__(self, message):
        super().__init__({
            'message': message
        })
        self.status_code = 444

