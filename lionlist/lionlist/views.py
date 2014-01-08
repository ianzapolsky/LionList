from django.shortcuts import render

def error404(request):
    return render(request, '404.html')

def error500(request):
    return render(request, '500.html')
