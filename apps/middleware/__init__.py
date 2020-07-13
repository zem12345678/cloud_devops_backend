from django.utils.deprecation import MiddlewareMixin



class CusMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        print('中间件方法 process_request 被调用')

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print('中间件方法 process_view 被调用')

    def process_response(self, request, response):
        print('中间件方法 process_response 被调用')
        return response

    def process_exception(self, request, exception):
        print('中间件方法 process_exception 被调用')

    def process_template_response(self, request, response):
        print('中间件方法 process_template_response 被调用')
        return response