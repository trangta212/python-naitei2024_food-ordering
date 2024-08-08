from django.shortcuts import render


def index(request):
    """View function for home page of site."""
    context = {
    }
    return render(request, 'index.html', context=context)
