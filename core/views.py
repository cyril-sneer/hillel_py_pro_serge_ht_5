from django.shortcuts import render


def page_not_found_view(request, exception):
    # return HttpResponseNotFound('Page not found')
    return render(request, 'exceptions/404.html', status=404)
