from django.http import HttpResponseNotFound
from django.urls import reverse

from catalog.models import LogModel


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        admin_url = reverse("admin:index")
        if not request.path.startswith(admin_url):
            log_record = LogModel(
                path=request.path,
                method=request.method,
                status=response.status_code,
                query_get=request.GET,
                body_post=request.POST,
                # timestamp will be added automatically
            )
            log_record.save()

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        pass
        # admin_url = reverse("admin:index")
        # if not request.path.startswith(admin_url):
        #     log_record = LogModel(
        #         path=request.path,
        #         method=request.method,
        #         status=200,
        #         query_get=request.GET,
        #         body_post=request.POST,
        #         # timestamp will be added automatically
        #     )
        #     log_record.save()

    def process_exception(self, request, exception):
        if 'No Person matches the given query.' in exception.args:
            return HttpResponseNotFound('User not found')
