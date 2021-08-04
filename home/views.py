from django.shortcuts import render
from productstore.models import Product

# Create your views here.


def index(request):
    """ A view to return the index page """
    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
    }

    return render(request, 'home/index.html', context)
