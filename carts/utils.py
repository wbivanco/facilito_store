from .models import Cart

def get_or_create_cart(request):
	# Verifico si está logeado sino genera None
	user = request.user if request.user.is_authenticated else None
	# Traigo el cart_id o None que es el identificador y no el id
	cart_id = request.session.get('cart_id')
	# Traigo el carrito con cart_id o None
	cart = Cart.objects.filter(cart_id=cart_id).first()

	# Si no existe el carrito lo creo
	if cart is None:		
		cart = Cart.objects.create(user=user)

	# Asigno un usuario al carrito ya creado
	if user and cart.user is None:
		cart.user = user
		cart.save()

	request.session['cart_id'] = cart.cart_id

	return cart