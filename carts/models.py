from django.db import models
import uuid
import decimal
from django.db.models.signals import pre_save
from django.db.models.signals import m2m_changed

from users.models import User
from products.models import Product


class Cart(models.Model):
	cart_id = models.CharField(max_length=100, null=False, blank=False, unique=True)
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
	products = models.ManyToManyField(Product, through='CartProducts')
	subtotal = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
	total = models.DecimalField(default=0.0, max_digits=8, decimal_places=2)
	created_at = models.DateTimeField(auto_now_add=True)

	FEE = 0.05

	def __str__(self):
		return self.cart_id

	def update_totals(self):
		self.update_subtotal()
		self.update_total()

	def update_subtotal(self):
		self.subtotal = sum([ product.price for product in self.products.all() ])
		self.save()

	def update_total(self):
		self.total = self.subtotal + (self.subtotal * decimal.Decimal(Cart.FEE))
		self.save()

	# Permite obtener todos lo objetos de una relación es como hacer 2 join juntos
	def product_related(self):
		return self.cartproducts_set.select_related('product')


class CartProducts(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	products = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	created_at = models.DateTimeField(auto_now_add=True)

# Creo un callback que unicamente cree el cart si no hay un carrito creado 
def set_cart_id(sender, instance, *args, **kwargs):
	if not instance.cart_id:
		# Genero un string unico
		instance.cart_id = str(uuid.uuid4())

# Creo el callback para actualizar el submtotal y el total del carrito de compras
def update_totals(sender, instance, action, *args, **kwargs):
	# El callback se dispara cuando alguno de las siguientes acciones se ejecutan 
	if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
		instance.update_totals()

# Vinculo el callbak de creación del cart con el signal
pre_save.connect(set_cart_id, sender=Cart)
# Vinculo el callback de calculo de subtotal y total con el signal
m2m_changed.connect(update_totals, sender=Cart.products.through)