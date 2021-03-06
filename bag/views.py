from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from productstore.models import Product
from .models import Bag, BagItem
from django.contrib.auth.decorators import login_required

# Create your views here.


def _bag_id(request):
    bag = request.session.session_key
    if not bag:
        bag = request.session.create()
    return bag


def add_bag(request, product_id):
    # fetching the Product by it's id
    product = Product.objects.get(id=product_id)
    try:
        # fetching the Bag by it's id from the session variable
        bag = Bag.objects.get(bag_id=_bag_id(request))
    except Bag.DoesNotExist:
        bag = Bag.objects.create(
            bag_id=_bag_id(request))
    bag.save()

    # Bag item

    try:
        bag_item = BagItem.objects.get(product=product, bag=bag)
        bag_item.quantity += 1
        bag_item.save()
    except BagItem.DoesNotExist:
        bag_item = BagItem.objects.create(
            product=product,
            quantity=1,
            bag=bag,
        )
        bag_item.save()
    return redirect('bag')


# remove the item quantity
def remove_bag(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    bag = Bag.objects.get(bag_id=_bag_id(request))
    bag_item = BagItem.objects.get(product=product, bag=bag)
    if bag_item.quantity > 1:
        bag_item.quantity -= 1
        bag_item.save()
    else:
        bag_item.delete()
    return redirect('bag')


# remove the whole bag item
def remove_bag_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    bag = Bag.objects.get(bag_id=_bag_id(request))
    bag_item = BagItem.objects.get(product=product, bag=bag)
    bag_item.delete()
    return redirect('bag')


def bag(request, total=0, quantity=0, bag_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            bag_items = BagItem.objects.filter(user=request.user, is_active=True)
        else:
            bag = Bag.objects.get(bag_id=_bag_id(request))
            bag_items = BagItem.objects.filter(bag=bag, is_active=True)
        for bag_item in bag_items:
            total += (bag_item.product.price * bag_item.quantity)
            quantity += bag_item.quantity
        tax = (13 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass  # just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'bag_items': bag_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'products/bag.html', context)


@login_required(login_url='/accounts/login')
def checkout(request, total=0, quantity=0, bag_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            bag_items = BagItem.objects.filter(user=request.user, is_active=True)
        else:
            bag = Bag.objects.get(bag_id=_bag_id(request))
            bag_items = BagItem.objects.filter(bag=bag, is_active=True)
        for bag_item in bag_items:
            total += (bag_item.product.price * bag_item.quantity)
            quantity += bag_item.quantity
        tax = (13 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass  # just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'bag_items': bag_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'products/checkout.html', context)
