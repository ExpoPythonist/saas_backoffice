from django.http import HttpResponse
from django.views import View


class HomePageView(View):
    def get(self, request):
        return HttpResponse('Hello')
