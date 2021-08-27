from django.shortcuts import render
from django.http import request

def vwIndex(request):
    return render(request, "index.html")