from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, get_user_model, logout
from .models import Perfil

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')


def registro(request):
    try:
        if request.method == 'POST':
            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            usuario = request.POST.get('usuario')
            correo  = request.POST.get('correo')
            password1 =request.POST.get('password1')
            password2 = request.POST.get('password2')
            if nombre == "" or usuario =="" or correo == "" or apellido == "" or password1 == "" or password2 == "":
                 return render(request, 'registro.html', {'mensaje': 'Ningún campo debe estar vacío'})
            else: 
                if password1 == password2:
                    if password1 and password2 and (len(password1) < 8 or len(password1) > 25 or len(password2) < 8 or len(password2) > 25):
                        return render(request, 'registro.html', {'mensaje': 'Las contraseñas deben tener minimo 8 caracteres y máximo 25'})
                    else:
                        user = User.objects.create_user(first_name=nombre, last_name=apellido, username=usuario, email=correo, password=password1)
                        Perfil.objects.create(user=user)
                        return render(request, 'index.html', {'mensaje': 'Usuario creado correctamente'})
                else:
                    return render(request, 'registro.html', {'mensaje': 'Las contraseñas no coinciden'})
        elif request.method== 'GET':
            return render(request, 'registro.html')
        
    except IntegrityError:
        return render (request, 'registro.html', {'mensaje': 'El usuario ya existe'} )
    except ValueError:
        return render(request,'registro.html',{'mensaje':'Dato no válido'})
    except Exception as error:
        print(error)


def iniciar_sesion(request):
    try:
        if request.method == 'POST':
            usuario = request.POST.get('usuario')
            password = request.POST.get('password1')
            User = get_user_model()
            try:
              user = User.objects.get(username=usuario)
            except User.DoesNotExist:
                user = None
            if user is None:
                return render(request,'login.html', {'mensaje': 'El usuario ingresado no existe'})
            else:
                user = authenticate(request, username=usuario, password=password)
                if user is not None: 
                    login (request, user)
                    return render(request, 'home.html')
                else:
                    return render(request, 'login.html',{'mensaje': 'Contraseña incorrecta'})
                
        elif request.method == 'GET':
            return render(request, 'login.html')
        
    except Exception as error:
        print(error)
        
def modificar(request, username):
    try:
        user = get_object_or_404(User, username=username)
        nombre = request.POST.get('nombre1')
        apellido = request.POST.get('apellido1')
        usuario = request.POST.get('usuario')
        correo = request.POST.get('email1')
        foto   = request.FILES.get('imagen')
        if request.user.is_authenticated:
            if request.method == 'POST':
                if nombre:
                    user.first_name = nombre
                    user.save()
                if apellido:
                    user.last_name = apellido
                    user.save()
                if usuario:
                    user.username = usuario
                    user.save()
                if correo:
                    user.email = correo
                    user.save()
                if foto:
                    perfil = Perfil.objects.get_or_create(user=user)
                    perfil.imagen = foto
                    perfil.save()
                    user.save()

                return redirect('perfil')
            return render(request, 'modificar_perfil.html')
    except IntegrityError:
        return render(request, 'modificar.html',{'mensaje':'Nombre de usuario ya existe'})
    except Exception as error:
        print(error)
        
def eliminar_usuario(request, username):
    usuario = get_object_or_404(User, username=username)
    usuario.delete()
    return redirect('inicio')

def cerrar_sesion(request):
    logout(request)
    return render(request, 'index.html')

def perfil(request):
    perfil = get_object_or_404(Perfil, user=request.user)
    return render(request, 'perfil.html', {'perfil': perfil})


