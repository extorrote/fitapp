
from django.contrib import admin
from django.urls import path,include
from fitapp import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static




####################################################################3

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='index'),
    path('index/', views.home, name='index'),
    path('biografia_javier/',views.biografia_javier,name="biografia_javier"),
    path('biografia_alejandro/',views.biografia_alejandro,name="biografia_alejandro"),
    path('registrar/', views.registro_usuario, name='registrar_usuario'),
    path('login/', views.login_view, name='login'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),
    path('logout/', views.logout_view, name='logout'),
    path('agregar_atleta/', views.agregar_atleta, name='agregar_atleta'),
    path('lista_atletas/', views.lista_atletas,name="lista_atletas"),
    path('editar_atleta/<int:id>/', views.editar_atleta,name="editar_atleta"),
    path('eliminar_atleta/<int:id>/', views.eliminar_atleta,name="eliminar_atleta"),
    #######################URLS PARA LOS PAQUETES

    path('crear-paquete/', views.crear_paquete, name='crear_paquete'),
    path('paquete/<int:pk>/editar/', views.editar_paquete, name='editar_paquete'),
    path('paquete/<int:pk>/eliminar/', views.eliminar_paquete, name='eliminar_paquete'),

    path("ckeditor5/", include("django_ckeditor_5.urls")),#############ESTO ES PAARA EL CHECKEDITOR
    path('paquete/<int:paquete_id>/agregar-dieta/', views.agregar_dieta, name='agregar_dieta'),
    path('paquete/<int:paquete_id>/agregar-rutina/', views.agregar_rutina, name='agregar_rutina'),
    path('dieta/<int:pk>/editar/', views.editar_dieta, name='editar_dieta'),
    path('dieta/<int:pk>/eliminar/', views.eliminar_dieta, name='eliminar_dieta'),
    path('rutina/<int:pk>/editar/', views.editar_rutina, name='editar_rutina'),
    path('rutina/<int:pk>/eliminar/', views.eliminar_rutina, name='eliminar_rutina'),   
    path('dieta/<int:pk>/detalle/', views.ver_detalle_dieta, name='ver_detalle_dieta'),
    path('rutina/<int:pk>/detalle/', views.ver_detalle_rutina, name='ver_detalle_rutina'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('iniciar_pago/<int:paquete_id>/', views.iniciar_pago, name='iniciar_pago'),
    path('pago_exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('pago_cancelado/', views.pago_cancelado, name='pago_cancelado'),
    path('ver_detalle_dieta_user/<int:pk>/detalle_user/', views.ver_detalle_dieta_user, name='ver_detalle_dieta_user'),
    path('ver_detalle_rutina_user/<int:pk>/detalle_user/', views.ver_detalle_rutina_user, name='ver_detalle_rutina_user'),
    
    
    
    
    

    
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/actualizar/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),

    
    
    path('agregar-al-carrito/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('ajax/tallas_por_color/', views.obtener_tallas_por_color, name='tallas_por_color'),

    path('direccion-envio/', views.direccion_envio, name='direccion_envio'),
    path('crear-sesion-pago/', views.crear_sesion_pago, name='crear_sesion_pago'),
    path('compra_exitosa/', views.compra_exitosa, name='compra_exitosa'),  # ← corregido aquí
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('tienda/', views.tienda, name='tienda'),
    path('enviar_email/', views.send_email, name="enviar_email"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



