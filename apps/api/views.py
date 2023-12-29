# from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def index(request):
    """Test endpoint"""
    return JsonResponse({"message": "API Root"}, safe=False)