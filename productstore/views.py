from django.shortcuts import render, get_object_or_404
from productstore.models import Product
from category.models import Category
from bag.models import BagItem
from bag.views import _bag_id
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Create your views here.


def all_products(request, category_slug=None):
    categories = None
    products = None
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=categories, is_available=True)
        # Pagination
        paginator = Paginator(products, 2)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        """ A view to show products page """

        products = Product.objects.all().filter(is_available=True)
        # Pagination
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(
            category__slug=category_slug, slug=product_slug)
        in_bag = BagItem.objects.filter(
            bag__bag_id=_bag_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_bag': in_bag,
    }
    return render(request, 'products/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by(
                '-created_at').filter(
                    Q(description__icontains=keyword) | Q(
                        product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'products/products.html', context)
