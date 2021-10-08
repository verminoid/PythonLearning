""" views module """
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


def simple_route(request):
    """ module """
    response = HttpResponse()
    if request.method != 'GET':
        response.status_code = 405
    else:
        response.status_code = 200
    return response


def slug_route(request):
    """ module """
    response = HttpResponse()
    body = request.path.split("/")[3]
    response.status_code = 200
    response.write(body)
    return response


def sum_route(request):
    """ module """
    response = HttpResponse()
    body = request.path.split("/")
    sum = int(body[3])+int(body[4])
    response.status_code = 200
    response.write(sum)
    return response


def isint(s):
    """ module """
    try:
        int(s)
        return True
    except ValueError:
        return False


@require_http_methods(["GET"])
def sum_get_method(request):
    """ module """
    response = HttpResponse()
    try:
        a = request.GET["a"]
        b = request.GET["b"]
        if (isint(a) and isint(b)):
            sum = int(a)+int(b)
            response.status_code = 200
            response.write(sum)
        else:
            response.status_code = 400
    except KeyError:
        response.status_code = 400
    return response


@require_http_methods(["POST"])
def sum_post_method(request):
    """ module """
    response = HttpResponse()
    try:
        a = request.POST["a"]
        b = request.POST["b"]
        if (isint(a) and isint(b)):
            sum = int(a)+int(b)
            response.status_code = 200
            response.write(sum)
        else:
            response.status_code = 400
    except KeyError:
        response.status_code = 400
    return response
