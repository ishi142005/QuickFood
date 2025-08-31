from django.shortcuts import render

def home(request):
    return render(request, 'quickfood/home.html')  # Include 'quickfood' as the folder prefix
