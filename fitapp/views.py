import stripe

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import (
    login, authenticate, logout, update_session_auth_hash
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    UserCreationForm, PasswordChangeForm
)
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models import Case, When, Value, IntegerField
from django.http import Http404, JsonResponse
from django.shortcuts import (
    render, redirect, get_object_or_404
)
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from fitapp.models import CompraPaquete

from .forms import (
    UserRegistrationForm, RegistroMujerForm, UserEditForm, AtletaForm,
    PaqueteForm, ContenidoDietaForm, ContenidoRutinaForm, DireccionDeEnvioForm
)
from .models import (
    RegistroUsuario, Paquete, ContenidoDieta, ContenidoRutina,
    NuestrosAtletas, CompraPaquete, SuplementosYFarmacos, Producto,
    VarianteProducto, Compra, DireccionDeEnvio, CarritoItem, CompraItem,
    TallaCalzado, TallaRopa, User  # Si "User" es un modelo personalizado en tu app
)
from django.contrib.auth import login as auth_login #SIN ESTO NO ME DEJA INICIAR SESION CON CUENTAS QUE LLEVAN MAS INFO DE LA INFO POR DEFECTO QUE TIENE user



def home(request):
    return render(request, 'index.html')



def registro_usuario(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = RegistroMujerForm(request.POST, request.FILES)  # request.FILES for foto_perfil

        if user_form.is_valid() and profile_form.is_valid():
            # Save user form
            user = user_form.save()

            # Create profile but don't save yet
            profile = profile_form.save(commit=False)
            profile.user = user  # Link User to RegistroUsuario

            # Save profile
            profile.save()

            # Auto-login (optional)
            login(request, user)

            messages.success(request, 'Usuario registrado exitosamente.')
            return redirect('index')  # Change to your actual home/dashboard view name

        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        user_form = UserRegistrationForm()
        profile_form = RegistroMujerForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'registro_usuarios.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)  # ✅ this uses the correct login function
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'login.html')







@login_required
def perfil_usuario(request):
    try:
        perfil = RegistroUsuario.objects.get(user=request.user)
    except RegistroUsuario.DoesNotExist:
        perfil = None  # Could redirect or show a message

    return render(request, 'perfil_usuario.html', {'perfil': perfil})



@login_required
def editar_perfil(request):
    user = request.user
    profile = get_object_or_404(RegistroUsuario, user=user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = RegistroMujerForm(request.POST, request.FILES, instance=profile)

        user_form.fields['username'].disabled = True

        if user_form.is_valid() and profile_form.is_valid():
            # 🔐 Check if password was changed
            password = user_form.cleaned_data.get("password")
            user = user_form.save()

            if password:
                logout(request)
                messages.success(request, "Has cambiado tu contraseña. Por seguridad, vuelve a iniciar sesión.")
                return redirect('login')  # Replace with your login view name
            else:
                update_session_auth_hash(request, user)

            # Save the profile
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')

    else:
        user_form = UserEditForm(instance=user)
        profile_form = RegistroMujerForm(instance=profile)
        user_form.fields['username'].disabled = True

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'registro_usuarios.html', context)



def logout_view(request):
    logout(request)
    return redirect('index') 




        
def agregar_atleta(request):
    if request.method == "POST":
        form=AtletaForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_atletas')#SI TODO SALE BIEN GUARDA Y REDIRECCIONA A INDEX
    else:
        form = AtletaForm()#OSINO SIGUE EN LA MISMA PAGINA DEL FORM
    
    return render(request,'agregar_atleta.html',{'form':form})



def lista_atletas(request):
    atletas= NuestrosAtletas.objects.all()
    atletas=atletas
    return render(request,'lista_atletas.html',{'atletas':atletas})




def editar_atleta(request,id):
    atleta = get_object_or_404(NuestrosAtletas, id=id)
    if request.method == "POST":
        form=AtletaForm(request.POST,request.FILES,instance=atleta)
        if form.is_valid():
            form.save()
            return redirect('lista_atletas')
    else:
        form=AtletaForm(instance=atleta)
    
    return render(request,'agregar_atleta.html',{'form':form})



def eliminar_atleta(request,id):
    atleta=get_object_or_404(NuestrosAtletas,id=id)
    if atleta:
        atleta.delete()
        
        return redirect('lista_atletas')
    else:
        return ('Ocurrio un error')


@staff_member_required
def crear_paquete(request):
    if request.method == 'POST':
        form = PaqueteForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # redirige para crear otro o cambiar por donde quieras
    else:
        form = PaqueteForm()
    return render(request, 'crear_paquete.html', {'form': form})







@staff_member_required
def agregar_dieta(request, paquete_id):
    paquete = get_object_or_404(Paquete, pk=paquete_id)
    if request.method == 'POST':
        form = ContenidoDietaForm(request.POST, request.FILES)
        if form.is_valid():
            dieta = form.save(commit=False)
            dieta.paquete = paquete
            dieta.save()
            return redirect('admin_dashboard')
    else:
        form = ContenidoDietaForm()
    return render(request, 'crear_dieta.html', {'form': form, 'paquete': paquete})

@staff_member_required
def agregar_rutina(request, paquete_id):
    paquete = get_object_or_404(Paquete, pk=paquete_id)
    if request.method == 'POST':
        form = ContenidoRutinaForm(request.POST, request.FILES)
        if form.is_valid():
            rutina = form.save(commit=False)
            rutina.paquete = paquete
            rutina.save()
            return redirect('admin_dashboard')
    else:
        form = ContenidoRutinaForm()
    return render(request, 'crear_rutina.html', {'form': form, 'paquete': paquete})


#######AQUI ESTOY MOSTRANDO LOS PAQUETES
@staff_member_required
def admin_dashboard(request):
    paquetes = Paquete.objects.all().prefetch_related('dietas', 'rutinas')  

    return render(request, 'admin_dashboard.html', {
        'paquetes': paquetes,
    })
    


@staff_member_required
def editar_paquete(request, pk):
    paquete = get_object_or_404(Paquete, pk=pk)
    if request.method == "POST":
        form = PaqueteForm(request.POST,request.FILES, instance=paquete)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = PaqueteForm(instance=paquete)
    return render(request, 'crear_paquete.html', {'form': form})

# Similar para eliminar y para dietas y rutinas

@staff_member_required
def eliminar_paquete(request, pk):
    paquete = get_object_or_404(Paquete, pk=pk)
    paquete.delete()
    return redirect('admin_dashboard')




@staff_member_required
def editar_dieta(request, pk):
    dieta = get_object_or_404(ContenidoDieta, pk=pk)
    if request.method == "POST":
        form = ContenidoDietaForm(request.POST, request.FILES, instance=dieta)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ContenidoDietaForm(instance=dieta)
    return render(request, 'crear_dieta.html', {'form': form})

@staff_member_required
def eliminar_dieta(request, pk):
    dieta = get_object_or_404(ContenidoDieta, pk=pk)
    dieta.delete()
    return redirect('admin_dashboard')

@staff_member_required
def editar_rutina(request, pk):
    rutina = get_object_or_404(ContenidoRutina, pk=pk)
    if request.method == "POST":
        form = ContenidoRutinaForm(request.POST, request.FILES, instance=rutina)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ContenidoRutinaForm(instance=rutina)
    return render(request, 'crear_rutina.html', {'form': form})

@staff_member_required
def eliminar_rutina(request, pk):
    rutina = get_object_or_404(ContenidoRutina, pk=pk)
    rutina.delete()
    return redirect('admin_dashboard')





@staff_member_required
def ver_detalle_dieta(request, pk):
    dieta = get_object_or_404(ContenidoDieta, pk=pk)
    paquetes = Paquete.objects.all().prefetch_related('dietas', 'rutinas')
    return render(request, 'admin_dashboard.html', {
        'paquetes': paquetes,
        'detalle_dieta': dieta
    })

@staff_member_required
def ver_detalle_rutina(request, pk):
    rutina = get_object_or_404(ContenidoRutina, pk=pk)
    paquetes = Paquete.objects.all().prefetch_related('dietas', 'rutinas')
    return render(request, 'admin_dashboard.html', {
        'paquetes': paquetes,
        'detalle_rutina': rutina
    })





####################### ESTO ES PARA LOS PAQUETES ###########################3
@login_required
def iniciar_pago(request, paquete_id):
    paquete = Paquete.objects.get(id=paquete_id)

    # Crear la sesión de pago
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        customer_email=request.user.email,
        line_items=[{
            'price_data': {
                'currency': 'mxn', #AQUI LE ESTOY INDICANDO QUE MONEDA ES EL PRECIO DEL ITEM
                'product_data': {
                    'name': paquete.titulo,
                },
                'unit_amount': int(paquete.precio * 100),  # en centavos
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri('/pago_exitoso/') + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri('/pago_cancelado/'),
    )

    # Guardar la compra con el session_id para luego poder buscarla fácilmente
    CompraPaquete.objects.get_or_create(
        usuario=request.user,
        paquete=paquete,
        defaults={'stripe_session_id': session.id}
    )

    return redirect(session.url, code=303)

from django.core.mail import EmailMessage #ESTO LO DEBI IMPORTAR PARA PODER QUE SE ENVIE EL CONFIRMACION MENSAJE DESDE LA TEMPLATE 
@login_required
def pago_exitoso(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        return redirect('user_dashboard')

    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except stripe.error.InvalidRequestError:
        return render(request, 'pago_error.html', {
            'mensaje': 'Sesión de pago inválida o expirada. Contacta al soporte.'
        })

    try:
        compra = CompraPaquete.objects.get(usuario=request.user, stripe_session_id=session_id)
    except CompraPaquete.DoesNotExist:
        return render(request, 'pago_error.html', {
            'mensaje': 'No se pudo confirmar tu compra. Contacta al soporte.'
        })

    if session.payment_status == 'paid':
        compra.pagado = True
        compra.stripe_payment_intent = session.payment_intent
        compra.save()
        
        
        subject = "Nueva compra de paquete - Belmont Herrera"
        to_email = settings.APPOINTMENT_EMAIL
        from_email = settings.DEFAULT_FROM_EMAIL

        html_message = render_to_string('emails/notificacion_compra_paquete.html', {
            'usuario': request.user,
            'paquete': compra.paquete,
            'compra': compra,
            
        })
        email = EmailMessage(subject, html_message, from_email, [to_email])
        email.content_subtype = 'html'
        email.send(fail_silently=False)
        

    else:
        return render(request, 'pago_error.html', {
            'mensaje': 'El pago no se ha completado correctamente.'
        })

    return redirect('user_dashboard')
###############################################################################





@login_required
def pago_cancelado(request):
    return render(request, 'pago_cancelado.html')



@login_required
def ver_detalle_dieta_user(request, pk):
    dieta = get_object_or_404(ContenidoDieta, pk=pk)
    
    # Verificar si esta dieta está en algún paquete que compró el usuario
    paquetes_usuario = CompraPaquete.objects.filter(usuario=request.user, pagado=True).values_list('paquete__id', flat=True)
    
    # Verificar si la dieta pertenece a uno de esos paquetes
    tiene_acceso = Paquete.objects.filter(id__in=paquetes_usuario, dietas=dieta).exists()

    if not tiene_acceso and not request.user.is_staff:
        raise Http404("No tienes permiso para ver esta dieta.")

    paquetes = Paquete.objects.all().prefetch_related('dietas', 'rutinas')

    return render(request, 'ver_detalle_dieta_user.html', {
        'paquetes': paquetes,
        'detalle_dieta': dieta
    })




@login_required
def ver_detalle_rutina_user(request, pk):
    rutina = get_object_or_404(ContenidoRutina, pk=pk)

    paquetes_usuario = CompraPaquete.objects.filter(usuario=request.user, pagado=True).values_list('paquete__id', flat=True)
    tiene_acceso = Paquete.objects.filter(id__in=paquetes_usuario, rutinas=rutina).exists()

    if not tiene_acceso and not request.user.is_staff:
        raise Http404("No tienes permiso para ver esta rutina.")

    paquetes = Paquete.objects.all().prefetch_related('dietas', 'rutinas')

    return render(request, 'ver_detalle_rutina_user.html', {
        'paquetes': paquetes,
        'detalle_rutina': rutina
    })





def biografia_javier(request):
    return render (request,'biografia_javier.html')


def biografia_alejandro(request):
    return render (request,'biografia_alejandro.html')




from .models import CarritoItem
# views.py

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(SuplementosYFarmacos, id=producto_id)
    cantidad = int(request.POST.get('cantidad', 1))

    item, created = CarritoItem.objects.get_or_create(usuario=request.user, producto=producto)
    if not created:
        item.cantidad += cantidad
    else:
        item.cantidad = cantidad
    item.save()

    return redirect('ver_carrito')





@login_required
def actualizar_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id, usuario=request.user)
    nueva_cantidad = int(request.POST.get('cantidad', 1))
    item.cantidad = nueva_cantidad
    item.save()
    return redirect('ver_carrito')


@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id, usuario=request.user)
    item.delete()
    return redirect('ver_carrito')







################ ESTO ME TOCO CREARLO PORQUE AL ACTUALIZAR LA TALLA ME ESTABA TIRANDO AL PRINCIPIO DE LA PAGINA Y CON ESTO MAS UN CODIGO JS EN LA TEMPLATE YA NO ME VA TIRAR ASI
from django.http import JsonResponse

@login_required
def obtener_tallas_por_color(request):
    producto_id = request.GET.get('producto_id')
    color = request.GET.get('color')

    tallas_data = []
    if producto_id and color:
        producto = Producto.objects.filter(id=producto_id).first()
        if producto:
            variantes = producto.variantes.filter(color=color)

            if producto.tipo == 'ropa':
                # obtener tallas únicas con stock sumado o filtrado
                talla_ids = variantes.exclude(talla_ropa__isnull=True).values_list('talla_ropa', flat=True).distinct()
                tallas = TallaRopa.objects.filter(id__in=talla_ids)
                for t in tallas:
                    stock_total = variantes.filter(talla_ropa=t).aggregate(total_stock=Sum('stock'))['total_stock'] or 0
                    tallas_data.append({'id': t.id, 'nombre': str(t), 'stock': stock_total})
            elif producto.tipo == 'calzado':
                talla_ids = variantes.exclude(talla_calzado__isnull=True).values_list('talla_calzado', flat=True).distinct()
                tallas = TallaCalzado.objects.filter(id__in=talla_ids)
                for t in tallas:
                    stock_total = variantes.filter(talla_calzado=t).aggregate(total_stock=Sum('stock'))['total_stock'] or 0
                    tallas_data.append({'id': t.id, 'nombre': str(t), 'stock': stock_total})

    return JsonResponse({'tallas': tallas_data})



from django.db.models import Q #ESTO LO AGREGAMOS PARA ADICIONAR QUE SE MUESTRE EN TODOS LOS PERFILES CUANDO UN PRODUCTO SE POSTEA CON META PERSONAL otro
from django.db.models import Sum
def user_dashboard(request):
    productos_en_carrito = CarritoItem.objects.filter(usuario=request.user)
    #ESTO LO AGREGUE PARA MOSTRAR LOS IEMS QUE HAY EN EL CARRITO
    items_en_carrito = CarritoItem.objects.filter(usuario=request.user).aggregate(total=Sum('cantidad'))['total'] or 0
    
    perfil = RegistroUsuario.objects.filter(user=request.user).first()
    lesiones_perfil= perfil.lesiones
    meta_usuario = perfil.meta_personal if perfil else None
    mostrar_solo_comprados = request.GET.get('solo_comprados') == 'true'
    color_seleccionado = request.GET.get('color')
    tallas_ropa = TallaRopa.objects.all()

    paquetes_con_acceso = CompraPaquete.objects.filter(
        usuario=request.user, pagado=True
    ).values_list('paquete_id', flat=True)

    if meta_usuario:
        if meta_usuario == 'otro':
            paquetes = Paquete.objects.all().prefetch_related('dietas', 'rutinas')
            farmacos_suplementos = SuplementosYFarmacos.objects.all()
        else:
            paquetes = Paquete.objects.filter(
                Q(meta_personal=meta_usuario) | Q(meta_personal='otro')
            ).prefetch_related('dietas', 'rutinas')
            farmacos_suplementos = SuplementosYFarmacos.objects.filter(
                Q(meta_personal=meta_usuario) | Q(meta_personal='otro')
            )

        paquetes_con_acceso_list = paquetes.filter(id__in=paquetes_con_acceso)
        paquetes_sin_acceso_list = paquetes.exclude(id__in=paquetes_con_acceso)

        if mostrar_solo_comprados:
            paquetes_con_acceso_list = paquetes_con_acceso_list
            paquetes_sin_acceso_list = Paquete.objects.none()

        productos = Producto.objects.prefetch_related('variantes').all()
        productos_info = []

        for producto in productos:
            variantes = producto.variantes.all()
            colores = variantes.values_list('color', flat=True).distinct()

            variantes_color = variantes.filter(color=color_seleccionado) if color_seleccionado else variantes

            if producto.tipo == 'ropa':
                talla_ids = variantes_color.exclude(talla_ropa__isnull=True).values_list('talla_ropa', flat=True).distinct()
                tallas = TallaRopa.objects.filter(id__in=talla_ids)
            elif producto.tipo == 'calzado':
                talla_ids = variantes_color.exclude(talla_calzado__isnull=True).values_list('talla_calzado', flat=True).distinct()
                tallas = TallaCalzado.objects.filter(id__in=talla_ids)
            else:
                tallas = []

            # Estructura de stock
            stock_por_talla_y_color = {}
            for var in variantes:
                talla = var.talla_ropa.codigo if producto.tipo == 'ropa' else str(var.talla_calzado)
                color = var.color
                stock = var.stock
                stock_por_talla_y_color.setdefault(color, {})[talla] = stock

            productos_info.append({
                'producto': producto,
                'colores': colores,
                'tallas': tallas,
                'stock_por_talla_y_color': stock_por_talla_y_color,
            })
    else:
        paquetes_con_acceso_list = Paquete.objects.none()
        paquetes_sin_acceso_list = Paquete.objects.none()
        farmacos_suplementos = SuplementosYFarmacos.objects.none()
        productos_info = []

    return render(request, 'user_dashboard.html', {
        'paquetes_con_acceso_list': paquetes_con_acceso_list,
        'paquetes_sin_acceso_list': paquetes_sin_acceso_list,
        'paquetes_con_acceso': paquetes_con_acceso,
        'mostrar_solo_comprados': mostrar_solo_comprados,
        'farmacos_suplementos': farmacos_suplementos,
        'productos_info': productos_info,
        'color_seleccionado': color_seleccionado,
        'tallas_ropa': tallas_ropa,
        'productos_en_carrito': productos_en_carrito,
        'items_en_carrito':items_en_carrito,
        'lesiones_perfil':lesiones_perfil,
    })





@require_POST
def agregar_al_carrito(request):
    producto_id = request.POST.get('producto_id')
    cantidad = int(request.POST.get('cantidad', 1))
    tipo = request.POST.get('content_type')
    color = request.POST.get('color')
    talla_seleccionada = request.POST.get('talla')

    if tipo == 'suplementos':
        modelo = SuplementosYFarmacos
        content_type = ContentType.objects.get_for_model(SuplementosYFarmacos)
        producto = get_object_or_404(modelo, pk=producto_id)

        CarritoItem.objects.create(
            usuario=request.user,
            content_type=content_type,
            object_id=producto.id,
            cantidad=cantidad,
            talla=None,
            color=None,
            variante=None
        )

    else:  # ropa o calzado
        producto = get_object_or_404(Producto, pk=producto_id)
        variantes = producto.variantes.filter(color=color)

        # Dependiendo del tipo, buscar variante que tenga esa talla
        if producto.tipo == 'ropa':
            variante = variantes.filter(talla_ropa__id=talla_seleccionada).first()
        elif producto.tipo == 'calzado':
            variante = variantes.filter(talla_calzado__id=talla_seleccionada).first()
        else:
            variante = None

        if not variante:
            # Variante no encontrada, manejar error o redirigir con mensaje
            # Aquí solo redirijo simple, pero puedes usar messages framework para alertar
            return redirect('user_dashboard')

        content_type = ContentType.objects.get_for_model(producto.__class__)

        CarritoItem.objects.create(
            usuario=request.user,
            content_type=content_type,
            object_id=producto.id,
            cantidad=cantidad,
            variante=variante,
            talla=str(variante.talla_ropa or variante.talla_calzado or ''),
            color=variante.color,
        )

    return redirect('ver_carrito')


@login_required
def ver_carrito(request):
    carrito_items = CarritoItem.objects.filter(usuario=request.user).select_related('content_type')

    if request.method == 'POST':
        for item in carrito_items:
            nueva_cantidad = request.POST.get(f'cantidad_{item.id}')
            color_seleccionado = request.POST.get(f'color_{item.id}')
            variante_id_seleccionada = request.POST.get(f'talla_{item.id}')  # ID de variante seleccionada

            if nueva_cantidad:
                nueva_cantidad = int(nueva_cantidad)

                if item.es_ropa_o_calzado and hasattr(item.producto, 'variantes'):
                    if variante_id_seleccionada:
                        variante = item.producto.variantes.filter(id=variante_id_seleccionada).first()
                        if variante:
                            # Verificar stock
                            stock_disponible = variante.stock or 0
                            if nueva_cantidad > stock_disponible:
                                nueva_cantidad = stock_disponible

                            item.variante = variante
                            item.color = variante.color
                            if item.producto.tipo == 'ropa':
                                item.talla = variante.talla_ropa.codigo if variante.talla_ropa else None
                            elif item.producto.tipo == 'calzado':
                                item.talla = str(variante.talla_calzado) if variante.talla_calzado else None

                item.cantidad = nueva_cantidad
                item.save()
        return redirect('ver_carrito')

    productos = []

    for item in carrito_items:
        producto = item.producto
        colores = []
        tallas = []
        stock_por_talla_y_color = {}

        if item.es_ropa_o_calzado and hasattr(producto, 'variantes'):
            variantes = producto.variantes.all()
            colores = variantes.values_list('color', flat=True).distinct()

            if producto.tipo == 'ropa':
                talla_ids = variantes.exclude(talla_ropa__isnull=True).values_list('talla_ropa', flat=True).distinct()
                tallas = TallaRopa.objects.filter(id__in=talla_ids)
            elif producto.tipo == 'calzado':
                talla_ids = variantes.exclude(talla_calzado__isnull=True).values_list('talla_calzado', flat=True).distinct()
                tallas = TallaCalzado.objects.filter(id__in=talla_ids)

            # Este es el bloque importante que estructura el stock por talla y color
            for var in variantes:
                color = var.color
                talla = None
                if producto.tipo == 'ropa' and var.talla_ropa:
                    talla = var.talla_ropa.codigo
                elif producto.tipo == 'calzado' and var.talla_calzado:
                    talla = str(var.talla_calzado)

                if color and talla:
                    if color not in stock_por_talla_y_color:
                        stock_por_talla_y_color[color] = {}
                    stock_por_talla_y_color[color][talla] = var.stock or 0

        productos.append({
            'item': item,
            'producto': producto,
            'es_ropa_o_calzado': item.es_ropa_o_calzado,
            'colores': colores,
            'tallas': tallas,
            'stock_por_talla_y_color': stock_por_talla_y_color,
        })

    total = sum(item.subtotal() for item in carrito_items)

    return render(request, 'carrito.html', {
        'productos_en_carrito': productos,
        'total': total,
    })






def calcular_costo_envio(productos, opcion_entrega, pais='México'):
    # Asegurar que 'productos' sea siempre una lista
    if not isinstance(productos, (list, tuple)):
        productos = [productos]

    if not productos:
        return 0

    # Envío internacional: solo se toma el mayor costo de envío internacional
    if pais.strip().lower() != 'méxico':
        costos_internacionales = [
            p.precio_envio_internacional or 0 for p in productos if not p.tiene_envio_gratis
        ]
        return max(costos_internacionales) if costos_internacionales else 0

    # Envío nacional: tomar el mayor costo por opción de entrega
    costos_nacionales = []

    for producto in productos:
        if producto.tiene_envio_gratis:
            continue

        if opcion_entrega == 'domicilio':
            costos_nacionales.append(producto.precio_envio_domicilio or 0)
        elif opcion_entrega == 'domicilio_express':
            costos_nacionales.append(producto.precio_envio_express_domicilio or 0)
        elif opcion_entrega == 'sucursal':
            costos_nacionales.append(producto.precio_envio_sucursal or 0)
        elif opcion_entrega == 'sucursal_express':
            costos_nacionales.append(producto.precio_envio_express_sucursal or 0)

    return max(costos_nacionales) if costos_nacionales else 0





@login_required
def direccion_envio(request):
    carrito_items = CarritoItem.objects.filter(usuario=request.user)
    if not carrito_items.exists():
        return redirect('ver_carrito')

    productos = [item.producto for item in carrito_items]

    # Detectar si todos los productos tienen envío gratis
    todos_envio_gratis = all(p.tiene_envio_gratis for p in productos)

    if request.method == 'POST':
        form = DireccionDeEnvioForm(request.POST)
        if form.is_valid():
            direccion = form.save(commit=False)
            direccion.usuario = request.user

            # Solo bloquear express si TODOS tienen envío gratis
            if todos_envio_gratis and direccion.opcion_entrega in ['domicilio_express', 'sucursal_express']:
                form.add_error(
                    'opcion_entrega',
                    'Las opciones de envío express no están disponibles cuando todos los productos tienen envío gratis.'
                )
            else:
                costo_envio = calcular_costo_envio(
                    productos=productos,
                    opcion_entrega=direccion.opcion_entrega,
                    pais=direccion.pais
                )
                direccion.costo_envio = costo_envio
                direccion.save()
                request.session['direccion_envio_id'] = direccion.id
                return redirect('crear_sesion_pago')
    else:
        form = DireccionDeEnvioForm()

    return render(request, 'formulario_envio.html', {
        'form': form,
        'todos_envio_gratis': all(p.tiene_envio_gratis for p in productos)
    })




stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def crear_sesion_pago(request):
    carrito_items = CarritoItem.objects.filter(usuario=request.user)
    if not carrito_items.exists():
        messages.error(request, "Tu carrito está vacío.")
        return redirect('ver_carrito')

    direccion_id = request.session.get('direccion_envio_id')
    if not direccion_id:
        messages.error(request, "No se encontró la dirección de envío.")
        return redirect('direccion_envio')

    try:
        direccion = DireccionDeEnvio.objects.get(id=direccion_id, usuario=request.user)
    except DireccionDeEnvio.DoesNotExist:
        messages.error(request, "La dirección de envío no es válida.")
        return redirect('direccion_envio')

    # Calcular totales
    total_productos = sum(item.subtotal() for item in carrito_items)
    costo_envio = direccion.costo_envio or 0

    # Preparar items para Stripe con cantidad y precio unitario
    line_items = []
    for item in carrito_items:
        cantidad = item.cantidad if item.cantidad > 0 else 1
        precio_unitario = item.subtotal() / cantidad
        line_items.append({
            'price_data': {
                'currency': 'mxn',
                'product_data': {
                    'name': item.producto.titulo,
                },
                'unit_amount': int(precio_unitario * 100),  # Precio unitario en centavos
            },
            'quantity': cantidad,
        })

    # Agregar envío si aplica, mostrando el método elegido
    if costo_envio > 0:
        # Asumiendo que DireccionDeEnvio tiene 'opcion_entrega' y un dict OPCIONES_ENTREGA con nombres legibles
        metodo_envio = getattr(direccion, 'opcion_entrega', 'Costo de envío')
        if hasattr(DireccionDeEnvio, 'OPCIONES_ENTREGA'):
            metodo_envio = dict(DireccionDeEnvio.OPCIONES_ENTREGA).get(direccion.opcion_entrega, metodo_envio)

        line_items.append({
            'price_data': {
                'currency': 'mxn',
                'product_data': {'name': f'Envío: {metodo_envio}'},
                'unit_amount': int(costo_envio * 100),
            },
            'quantity': 1,
        })

    # Crear sesión de Stripe
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        customer_email=request.user.email,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('compra_exitosa')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('ver_carrito')),
        metadata={
            'usuario_id': request.user.id,
            'direccion_id': direccion.id,
        },
    )

    return redirect(checkout_session.url)





@login_required
def compra_exitosa(request):
    session_id = request.GET.get('session_id')
    if not session_id:
        messages.error(request, 'No se proporcionó un ID de sesión válido.')
        return redirect('ver_carrito')

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status != 'paid':
            messages.error(request, 'El pago no se completó correctamente.')
            return redirect('ver_carrito')

        # Verifica si ya se creó esta compra
        if Compra.objects.filter(stripe_session_id=session.id).exists():
            compra = Compra.objects.get(stripe_session_id=session.id)
        else:
            usuario = request.user
            direccion_id = session.metadata.get('direccion_id')
            direccion = DireccionDeEnvio.objects.get(id=direccion_id, usuario=usuario)

            # Crear la compra
            compra = Compra.objects.create(
                usuario=usuario,
                direccion=direccion,
                pagado=True,
                stripe_session_id=session.id,
            )

            carrito_items = CarritoItem.objects.filter(usuario=usuario)

            for item in carrito_items:
                # Obtener el precio según el tipo de producto
                if item.variante:
                    precio_unitario = item.variante.precio
                elif hasattr(item.producto, 'precio') and item.producto.precio:
                    precio_unitario = item.producto.precio
                else:
                    precio_unitario = 0

                CompraItem.objects.create(
                    compra=compra,
                    content_type=item.content_type,
                    object_id=item.object_id,
                    cantidad=item.cantidad,
                    precio_unitario=precio_unitario,
                    variante=item.variante  # ✅ Se guarda la variante aquí
                )

                # 🔁 ACTUALIZACIÓN DE STOCK
                if item.variante:
                    if item.variante.stock is not None and item.variante.stock >= item.cantidad:
                        item.variante.stock -= item.cantidad
                        item.variante.save()
                else:
                    if hasattr(item.producto, 'stock') and item.producto.stock is not None:
                        item.producto.stock -= item.cantidad
                        item.producto.save()

            carrito_items.delete()

            # 📨 Enviar correo al usuario
            subject = 'Confirmación de tu compra en Belmont Herrera'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [usuario.email]
            context = {'compra': compra}
            html_content = render_to_string('emails/detalle_compra_suplemento.html', context)

            msg = EmailMultiAlternatives(subject, '', from_email, to_email)
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

        messages.success(request, '¡Gracias por tu compra!')
        return render(request, 'emails/detalle_compra_suplemento.html', {'compra': compra})

    except stripe.error.StripeError as e:
        messages.error(request, f'Hubo un error procesando tu pago: {e.user_message}')
        return redirect('ver_carrito')


########### ESTO EN REALIDAD NO LO ESTAMOS UTILIZANDO PERO SI TIENE MUCHAS VENTAJAS Y PROBABLEMENE LO INTEGRE EN UN FUTURO

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'TU_SECRET_WEBHOOK_DE_STRIPE'

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return JsonResponse({'error': 'Webhook inválido'}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        usuario_id = session['metadata']['usuario_id']
        direccion_id = session['metadata']['direccion_id']

        # Evitar duplicación si ya se procesó
        if Compra.objects.filter(stripe_session_id=session['id']).exists():
            return JsonResponse({'status': 'Ya procesado'})

        usuario = User.objects.get(id=usuario_id)
        direccion = DireccionDeEnvio.objects.get(id=direccion_id)

        compra = Compra.objects.create(
            usuario=usuario,
            direccion=direccion,
            pagado=True,
            stripe_session_id=session['id'],
        )

        carrito_items = CarritoItem.objects.filter(usuario=usuario)
        for item in carrito_items:
            CompraItem.objects.create(
                compra=compra,
                content_type=item.content_type,
                object_id=item.object_id,
                cantidad=item.cantidad,
                precio_unitario=item.producto.precio,
            )
            # Actualizar stock
            if hasattr(item.producto, 'stock') and item.producto.stock is not None:
                item.producto.stock -= item.cantidad
                item.producto.save()

        carrito_items.delete()

    return JsonResponse({'status': 'ok'})




def tienda(request):
    if request.user.is_authenticated:
        productos_en_carrito = CarritoItem.objects.filter(usuario=request.user)
        perfil = RegistroUsuario.objects.filter(user=request.user).first()
    else:
        productos_en_carrito = []
        perfil = None

    color_seleccionado = request.GET.get('color')
    tallas_ropa = TallaRopa.objects.all()

    farmacos_suplementos = SuplementosYFarmacos.objects.all()
    productos = Producto.objects.prefetch_related('variantes').all()

    productos_info = []

    for producto in productos:
        variantes = producto.variantes.all()
        colores = variantes.values_list('color', flat=True).distinct()

        variantes_color = variantes.filter(color=color_seleccionado) if color_seleccionado else variantes

        # Obtener tallas según tipo
        if producto.tipo == 'ropa':
            talla_ids = variantes_color.exclude(talla_ropa__isnull=True).values_list('talla_ropa', flat=True).distinct()
            tallas = TallaRopa.objects.filter(id__in=talla_ids)
        elif producto.tipo == 'calzado':
            talla_ids = variantes_color.exclude(talla_calzado__isnull=True).values_list('talla_calzado', flat=True).distinct()
            tallas = TallaCalzado.objects.filter(id__in=talla_ids)
        else:
            tallas = []

        # Estructura de stock por color y talla
        stock_por_talla_y_color = {}
        for var in variantes:
            talla = (
                var.talla_ropa.codigo if producto.tipo == 'ropa'
                else str(var.talla_calzado) if producto.tipo == 'calzado'
                else 'Única'
            )
            color = var.color
            stock = var.stock
            stock_por_talla_y_color.setdefault(color, {})[talla] = stock

        productos_info.append({
            'producto': producto,
            'colores': colores,
            'tallas': tallas,
            'stock_por_talla_y_color': stock_por_talla_y_color,
        })

    return render(request, 'tienda.html', {
        'farmacos_suplementos': farmacos_suplementos,
        'productos_info': productos_info,
        'color_seleccionado': color_seleccionado,
        'tallas_ropa': tallas_ropa,
        'productos_en_carrito': productos_en_carrito,
    })



from .forms import ContactForm


def send_email(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            
            # Process the form data, e.g., send an email
            send_mail(
                f'Contact Form Submission from {name}',
                f'Message: {message}\nPhone: {phone}\nEmail: {email}',
                'proyectodigitalmexico@gmail.com',  # From email
                ['proyectodigitalmexico@gmail.com'],  # To email
                fail_silently=False,
            )
            
            
            messages.success(request, 'Email Sent! (Mensaje Enviado), Pronto recibiras una respuesta')
            return redirect('index')
    else:
        form = ContactForm()

    return render(request, 'enviar_email.html', {'form': form})