from django.shortcuts import render

def hub_page(request):
    return render(request, 'hub_page.html')
