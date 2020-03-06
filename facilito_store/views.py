# Permite dar como respuesta un html renderizado
from django.shortcuts import render
# Permite redirijir
from django.shortcuts import redirect
# Permite dar respuesta a una peticion(texto)
#from django.http import HttpResponse

# Permite enviar mensajes al servidor
from django.contrib import messages
# Permite generar una sesion 
from django.contrib.auth import login
# Permite cerrar la session
from django.contrib.auth import logout
# Permite autenticar los valores del formulario
from django.contrib.auth import authenticate
# Permite acceder y manipular almodelo User
#from django.contrib.auth.models import User
from users.models import User

# Formularios
from .forms import RegisterForm

# Modelos
from products.models import Product

def index(request):

	products = Product.objects.all().order_by('-id')

	return render(request,'index.html',{
		'message':'Listado de productos', 
		'title': 'Productos', 
		'products': products,
		})

def login_view(request):
	if request.user.is_authenticated:
		return redirect('index')

	if request.method == 'POST':
		# POST es un diccionario por eso get()
		username = request.POST.get('username')
		password = request.POST.get('password')

		# Chequea si los datos pasados existen en la BD sino None
		user = authenticate(username=username, password=password)

		if user:
			# Genera la sesion para el usuario pasado
			login(request, user)
			messages.success(request, 'Bienvenido {}'.format(user.username))
			return redirect('index')
		else:
			messages.error(request, 'Usuario o contraseña no validos')


	return render(request, 'users/login.html', {})

def logout_view(request):
	logout(request)
	messages.success(request, 'Sesión cerrada exitosamente')
	return redirect('login')

def register(request):
	if request.user.is_authenticated:
		return redirect('index')

	form = RegisterForm(request.POST or None)

	if request.method == 'POST' and form.is_valid():
		user = form.save()

		if user:
			login(request, user)
			messages.success(request, 'Usuario creado exitosamente')
			return redirect('index')

	return render(request, 'users/register.html', {'form':form})