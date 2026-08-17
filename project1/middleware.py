import datetime

class RequestLoginMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
        print("Custom middleware initialized.")

    def __call__(self,request):
        print(f"Incoming Request:{request.path} at {datetime.datetime.now()}")
        response = self.get_response(request)
        print(f"Outgoing Response:{response.status_code} at {datetime.datetime.now()}")
        return response

class AdvanceMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        return self.get_response(request)

    def process_view(self,request,view_func,view_args,view_kwargs):
        print(f"Process_view called for {view_func.__name__}")

    def process_exception(self,request,exception):
        print(f"Exception caught in middleware: {exception}")

    def process_template_response(self,request,response):
        print("process_template_response called.")
        return response 

class FirstMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        print("First middleware before view")
        response = self.get_response(request)
        print("First middleware after view")
        return response
class SecondMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self,request):
        print("Second middleware before view")
        response = self.get_response(request)
        print("Second middleware after view")
        return response