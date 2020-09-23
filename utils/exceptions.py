from rest_framework.views import exception_handler
from rest_framework import status
from rest_framework.exceptions import APIException

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status'] = response.status_code  # 可添加status_code
        response.data['message'] = response.data['detail']  # 增加message这个key
        del response.data['detail']
    return response



class NotValid(APIException):
    status_code = status.HTTP_402_PAYMENT_REQUIRED
    default_detail = 'commited sql were not valid.'
    default_code = 'invalid'
