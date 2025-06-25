from django.contrib import admin
from .models import RegistroUsuario,NuestrosAtletas,SuplementosYFarmacos


admin.site.site_header = "Administración de Belmont Herrera"
admin.site.site_title = "Panel de Administración - Belmont Herrera"
admin.site.index_title = "Bienvenido al Panel de Gestión de Belmont Herrera"




@admin.register(RegistroUsuario)
class RegistroUsuarioAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'tu_nombre', 'last_name', 'genero', 'meta_personal']
    search_fields = ['user__username', 'email', 'tu_nombre', 'last_name']


@admin.register(NuestrosAtletas)
class RegisterAtletaAdmin(admin.ModelAdmin):
    list_display=['nombre']
    search_fields=['nombre']
    
    
    
    
    
from django.contrib import admin
from .models import Paquete, ContenidoDieta, ContenidoRutina

from django.contrib import admin
from .models import Paquete, ContenidoDieta, ContenidoRutina

from django.contrib import admin
from .models import Paquete, ContenidoDieta, ContenidoRutina,CompraPaquete

# Inlines para mostrar las dietas relacionadas con el paquete
class ContenidoDietaInline(admin.StackedInline):  # Puedes cambiar a TabularInline si prefieres otra presentación
    model = ContenidoDieta
    extra = 1  # Número de formularios vacíos para agregar nuevos

# Inlines para mostrar las rutinas relacionadas con el paquete
class ContenidoRutinaInline(admin.StackedInline):
    model = ContenidoRutina
    extra = 1

# Admin del modelo Paquete
@admin.register(Paquete)
class PaqueteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'precio')
    inlines = [ContenidoDietaInline, ContenidoRutinaInline]

# Admin individual para ContenidoDieta (opcional)
@admin.register(ContenidoDieta)
class ContenidoDietaAdmin(admin.ModelAdmin):
    list_display = ('titulo',  'paquete')

# Admin individual para ContenidoRutina (opcional)
@admin.register(ContenidoRutina)
class ContenidoRutinaAdmin(admin.ModelAdmin):
    list_display = ('titulo',  'paquete')



@admin.register(CompraPaquete)
class ContenidoRutinaAdmin(admin.ModelAdmin):
    list_display = ('paquete', 'usuario', 'fecha_compra','entregado','pagado')




from django.contrib import admin
from .models import (
    Producto, VarianteProducto,
    TallaRopa, TallaCalzado,
    SuplementosYFarmacos,
    DireccionDeEnvio,
    CarritoItem,
    Compra, CompraItem
)

# ------------ INLINES ------------

class VarianteProductoInline(admin.TabularInline):
    model = VarianteProducto
    extra = 1
    autocomplete_fields = ['talla_ropa', 'talla_calzado']
    fields = ('genero', 'color', 'talla_ropa', 'talla_calzado', 'precio', 'stock')

# ------------ MODELOS ------------

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'marca', 'tiene_envio_gratis')
    list_filter = ('tipo', 'tiene_envio_gratis')
    search_fields = ('titulo', 'descripcion', 'marca')
    inlines = [VarianteProductoInline]



@admin.register(TallaRopa)
class TallaRopaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descripcion')
    search_fields = ('codigo', 'descripcion')

@admin.register(TallaCalzado)
class TallaCalzadoAdmin(admin.ModelAdmin):
    list_display = ('genero', 'us', 'eu', 'cm')
    list_filter = ('genero',)
    search_fields = ('genero',)  # También puedes agregar 'us' o 'eu' si lo necesitas


@admin.register(SuplementosYFarmacos)
class SuplementosYFarmacosAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'meta_personal', 'marca', 'tipo_de_producto', 'precio', 'stock')
    list_filter = ('meta_personal', 'marca', 'tipo_de_producto')
    search_fields = ('titulo', 'descripcion', 'marca')

@admin.register(DireccionDeEnvio)
class DireccionDeEnvioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nombre_completo', 'ciudad', 'pais', 'fecha_creacion')
    search_fields = ('nombre_completo', 'direccion', 'ciudad', 'estado', 'pais')

"""
#ESTE LO ESTOY QUITANDO PORQUE EN REALIDAD NO LO OCUPO, ESTE SE ESTA USANDO SOLAMENTE TEMPORALMENTE PARA GUARDAR LOS ITEMS QUE EL #USUARIO AGREGA AL CARRO PERO YA QUE SE PAGAN DESAPARECEN 
@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'producto', 'cantidad', 'agregado')
    readonly_fields = ('agregado',)
    search_fields = ('usuario__username',)


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'pagado', 'envio_realizado', 'creado')
    list_filter = ('pagado', 'envio_realizado')
    search_fields = ('usuario__username',)
    readonly_fields = ('creado',)

@admin.register(CompraItem)
class CompraItemAdmin(admin.ModelAdmin):
    list_display = ('compra', 'producto', 'cantidad', 'precio_unitario')

"""

#AQUI ESTOY UNIFICANDO Compra y CompraItem




from django.contrib import admin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .models import Compra, CompraItem

# Inlines
class CompraItemInline(admin.TabularInline):
    model = CompraItem
    extra = 0
    readonly_fields = ('mostrar_producto', 'mostrar_variante')
    fields = ('mostrar_producto', 'content_type', 'object_id', 'cantidad', 'precio_unitario', 'mostrar_variante')

    def mostrar_producto(self, obj):
        return str(obj.producto) if obj.producto else "Sin producto"
    mostrar_producto.short_description = 'Producto'

    def mostrar_variante(self, obj):
        if not obj.variante:
            return "—"
        color = obj.variante.color or ""
        talla = ""
        if obj.variante.talla_ropa:
            talla = f"Talla: {obj.variante.talla_ropa.codigo}"
        elif obj.variante.talla_calzado:
            t = obj.variante.talla_calzado
            talla = f"Talla: US {t.us} / EU {t.eu} / {t.cm} cm"
        return f"{color} {talla}".strip()
    mostrar_variante.short_description = 'Variante (Color y Talla)'


def enviar_email_notificacion_envio(compra):
    asunto = f"Tu pedido de Belmont Herrera ha sido enviado 📦"
    destinatario = compra.usuario.email

    if not destinatario:
        return  # no enviar si el usuario no tiene email

    contexto = {
        'compra': compra,
    }

    cuerpo_html = render_to_string("emails/notificacion_envio.html", contexto)

    mensaje = EmailMultiAlternatives(
        subject=asunto,
        body="Tu pedido ha sido enviado.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[destinatario],
    )
    mensaje.attach_alternative(cuerpo_html, "text/html")
    mensaje.send()


@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'pagado', 'envio_realizado', 'creado', 'total_compra')
    list_filter = ('pagado', 'envio_realizado')
    search_fields = ('usuario__username',)

    readonly_fields = (
        'creado',
        'total_compra',
        'mostrar_nombre_completo', 'mostrar_telefono', 'mostrar_direccion',
        'mostrar_ciudad', 'mostrar_estado', 'mostrar_codigo_postal',
        'mostrar_pais', 'mostrar_opcion_entrega', 'mostrar_costo_envio',
    )

    inlines = [CompraItemInline]

    def save_model(self, request, obj, form, change):
        envio_previo = None
        if obj.pk:
            envio_previo = Compra.objects.get(pk=obj.pk).envio_realizado

        super().save_model(request, obj, form, change)

        if not envio_previo and obj.envio_realizado:
            enviar_email_notificacion_envio(obj)

    def total_compra(self, obj):
        return f"${obj.total:.2f}"
    total_compra.short_description = "Total de la compra"

    # Métodos para mostrar los datos de la dirección
    def mostrar_nombre_completo(self, obj):
        return obj.direccion.nombre_completo
    def mostrar_telefono(self, obj):
        return obj.direccion.telefono
    def mostrar_direccion(self, obj):
        return obj.direccion.direccion
    def mostrar_ciudad(self, obj):
        return obj.direccion.ciudad
    def mostrar_estado(self, obj):
        return obj.direccion.estado
    def mostrar_codigo_postal(self, obj):
        return obj.direccion.codigo_postal
    def mostrar_pais(self, obj):
        return obj.direccion.pais
    def mostrar_opcion_entrega(self, obj):
        return obj.direccion.get_opcion_entrega_display()
    def mostrar_costo_envio(self, obj):
        return f"${obj.direccion.costo_envio:.2f}"

    # Etiquetas legibles
    mostrar_nombre_completo.short_description = "Nombre completo"
    mostrar_telefono.short_description = "Teléfono"
    mostrar_direccion.short_description = "Dirección"
    mostrar_ciudad.short_description = "Ciudad"
    mostrar_estado.short_description = "Estado"
    mostrar_codigo_postal.short_description = "Código Postal"
    mostrar_pais.short_description = "País"
    mostrar_opcion_entrega.short_description = "Tipo de entrega"
    mostrar_costo_envio.short_description = "Costo de Envío"

    # Agrupar campos en secciones visuales
    fieldsets = (
        ("Información de la compra", {
            'fields': ('usuario', 'pagado', 'envio_realizado','notas_de_envio', 'creado', 'total_compra'),
        }),
        ("Dirección de envío", {
            'fields': (
                'mostrar_nombre_completo', 'mostrar_telefono', 'mostrar_direccion',
                'mostrar_ciudad', 'mostrar_estado', 'mostrar_codigo_postal',
                'mostrar_pais', 'mostrar_opcion_entrega', 'mostrar_costo_envio'
            ),
        }),
    )