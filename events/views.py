from django.http import HttpResponse


def robots_txt(request):
    return HttpResponse("User-agent: *\nAllow: /\n", content_type="text/plain")
