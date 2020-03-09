from django.shortcuts import render
# Para poder reireccionar
from django.shortcuts import redirect

# Crear una sesion,solo se necesita crear una nueva llave en el diccionario
#request.session['cart_id'] = '123'
# Recuperar una sesion
#request.session.get('cart_id')
# Eliminar una sesion
#request.session['cart_id'] = None

# Modelos
from .models import Cart
from products.models import Product

# Utilidades
from .utils import get_or_create_cart

def cart(request):
	cart = get_or_create_cart(request)

	return render(request, 'carts/cart.html',{'cart':cart})

def add(request):
	cart = get_or_create_cart(request)
	product = Product.objects.get(pk=request.POST.get('product_id'))

	cart.products.add(product)

	return render(request, 'carts/add.html', {
			'product': product
		})

def remove():
	cart = get_or_create_cart(request)
	product = Product.objects.get(pk=request.POST.get('product_id'))

	cart.products.remove(product)

	return redirect('carts:cart')