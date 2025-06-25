from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
##################### DEBI INSTALAR pip install django-ckeditor-5
# PARA QUE ESTO FUNCIONE DEBI TOCAR INSTALLED APPS, settings de media root, urls TAMBIEN EN FORMS.PY Y EN LA TEMPLATE DEBO PONER ESTO {{ form.media }} EN LA TEMPLATE , 
META_PERSONAL_CHOICES = [
    ('perdida_peso', 'Pérdida de peso'),
    ('masa_muscular', 'Aumento de masa muscular'),
    ('definicion', 'Definición (definición muscular)'),
    ('estetica', 'Estética (masa muscular/definición muscular)'), 
    ('rendimiento', 'Mejorar rendimiento físico'),
    ('fuerza', 'Fuerza'),  
    ('competencia', 'Competencia'),
    ('potencia_sexual', 'Aumentar potencia sexual'),
    ('longevidad', 'Longevidad'),
    ('otro', 'Otro'),
]

GENERO_CHOICES = [
    ('hombre', 'Hombre'),
    ('mujer', 'Mujer'),
    ('otro', 'Otro'),
]

TIPO_ABORTO_CHOICES = [
    ('natural', 'Natural'),
    ('inducido', 'Inducido'),
]

class RegistroUsuario(models.Model):  # Hereda de AbstractUser
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
    tu_nombre = models.CharField(max_length=255, blank=True, null=True,verbose_name='Nombre')
    last_name = models.CharField(max_length=255, blank=True, null=True,verbose_name='Apellidos')
    email = models.EmailField(blank=True, null=True, verbose_name='Correo Electrónico')
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)
    fecha_nacimiento = models.CharField(max_length=300, null=True, blank=True)
    estado_civil = models.CharField(max_length=50, blank=True, null=True)
    numero_telefono = models.CharField(max_length=20, blank=True, null=True)
    contacto_emergencia = models.CharField(max_length=20, blank=True, null=True)
    peso_actual = models.CharField(max_length=300, null=True, blank=True)
    altura = models.CharField(max_length=300, null=True, blank=True)
    enfermedades = models.CharField(max_length=300, null=True, blank=True)
    alergias = models.CharField(max_length=300, null=True, blank=True)
    medicamentos = models.CharField(max_length=300, null=True, blank=True)
    cirugias = models.CharField(max_length=300, null=True, blank=True)
    lesiones = models.BooleanField(default=False)
    tipo_de_lesiones=models.CharField(max_length=200,blank=True,null=True)
    tiempo_lesiones = models.CharField(max_length=100, blank=True, null=True,help_text="tipo y tiempo de lecciones")
    hijos = models.CharField(max_length=300, null=True, blank=True)
    rutina_diaria = models.CharField(max_length=500, blank=True, null=True)
    meta_personal = models.CharField(max_length=30, choices=META_PERSONAL_CHOICES, blank=True, null=True)
    interesado_dieta = models.BooleanField(default=False)
    interesado_entrenamiento = models.BooleanField(default=False)
    interesado_farmacologia = models.BooleanField(default=False)
    desea_atencion_personalizada = models.BooleanField(default=False)
    uso_farmacologia = models.CharField(max_length=300, null=True, blank=True)
    uso_suplementos = models.CharField(max_length=300, null=True, blank=True)
    ha_competido = models.BooleanField(default=False)
    numero_competiciones = models.CharField(max_length=300, null=True, blank=True)
    # Campos específicos para mujeres
    dias_regla = models.CharField(max_length=300, null=True, blank=True,help_text="Solo aplica si eres mujer")     
    irregular_promedio_3_meses = models.CharField(max_length=300, null=True, blank=True,help_text="Solo aplica si eres mujer")       
    esta_embarazada = models.BooleanField(default=False,help_text="Solo aplica si eres mujer")
    meses_embarazo = models.CharField(max_length=300, null=True, blank=True,)
    tiempo_postparto = models.CharField(max_length=100, null=True, blank=True,)
    ha_abortado = models.BooleanField(default=False,)
    tipo_aborto = models.CharField(max_length=20,choices=TIPO_ABORTO_CHOICES,blank=True, null=True,)
    
    #ESTO LO AGUEGUE PARA PODER MOSTRAR EL EMAIL QUE ESTOY SOLICITANDO EN FORMS PERO NO ES EL DE ESTE MODELO EN SI SINO EL DEL MODELO User
    def save(self, *args, **kwargs):
        # Sync email field with user model before saving
        self.email = self.user.email#ESTO LO HICE PARA QUE ESTOS CAMPOS APAREZCAN EN MI MODELO UserProfile pero en el form los estoy pidiendo del modelo User
        self.tu_nombre=self.user.first_name
        self.last_name=self.user.last_name
        super().save(*args, **kwargs)

    def __str__(self):
       
        return f"{self.user.username} ({self.genero})" 



class NuestrosAtletas(models.Model):
    nombre=models.CharField(max_length=100,blank=True,null=True)
    pais=models.CharField(max_length=200,null=True,blank=True,verbose_name="Pais")
    edad=models.CharField(max_length=100,blank=True,null=True)
    titulos_competitivos=models.CharField(max_length=200,blank=True,null=True)
    image1=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image2=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image3=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image4=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    descripcion=models.TextField(blank=True,null=True)
    class Meta:
        verbose_name="Nuestros Atletas"
        verbose_name_plural="Nuestros Atletas"
        
    def __str__(self):
        return f"{self.nombre}"



from django.utils.timezone import now
class Paquete(models.Model):
    TIPO_CHOICES = [
        ('rutina_basica', 'Rutina Básica'),
        ('dieta_basica', 'Dieta Básica'),
        ('completo_basico', 'Completo Básico (Dieta + Rutina)'),
        ('rutina_premium', 'Rutina Premium'),
        ('dieta_premium', 'Dieta Premium'),
        ('completo_premium', 'Completo Premium (Dieta + Rutina)'),
        ('completo_premium_con_farmacologia', 'Dieta + Rutina + Farmacologia'),
        
    ]
    meta_personal = models.CharField(max_length=100,blank=True,null=True, choices=META_PERSONAL_CHOICES)
    titulo=models.CharField(max_length=100,null=False,blank=False,default="")
    image1=models.ImageField(upload_to="images/paquetes",null=True,blank=True)
    categoria = models.CharField(max_length=50, choices=TIPO_CHOICES,verbose_name="Categoria de Paquete")
    descripcion = models.TextField()
    es_premium=models.BooleanField(default=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(default=now)
    class Meta:
        verbose_name="Lista de Paquetes en Tienda"
        verbose_name_plural="Lista de Paquetes en Tienda"
    def __str__(self):
        return self.get_categoria_display()



class ContenidoDieta(models.Model):
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE, related_name="dietas", null=True, blank=True)
    titulo = models.CharField(max_length=255,null=True, blank=True)
    
    semana1=models.CharField(max_length=100, default="SEMANA 1")
    image1=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image2=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image3=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image4=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image5=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image6=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    
    semana2=models.CharField(max_length=100,default="SEMANA 2")    
    image7=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image8=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image9=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image10=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image11=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image12=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    
    semana3=models.CharField(max_length=100,default="SEMANA 3")   
    image13=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image14=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image15=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image16=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image17=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image18=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    
    semana4=models.CharField(max_length=100,default="SEMANA 4")   
    image19=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image20=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image21=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image22=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image23=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image24=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    
    descripcion = CKEditor5Field('Contenido', config_name='default', default='')

    

    def __str__(self):
        return f"Dieta - {self.paquete} - {self.titulo}"

class ContenidoRutina(models.Model):
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE, related_name="rutinas", null=True, blank=True)
    titulo = models.CharField(max_length=255,null=True, blank=True)
    
    semana1=models.CharField(max_length=100, default="SEMANA 1")
    image1=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image2=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image3=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image4=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image5=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image6=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    
    semana2=models.CharField(max_length=100,default="SEMANA 2")    
    image7=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image8=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image9=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image10=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image11=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image12=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    
    semana3=models.CharField(max_length=100,default="SEMANA 3")   
    image13=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image14=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image15=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image16=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image17=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image18=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    
    semana4=models.CharField(max_length=100,default="SEMANA 4")   
    image19=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image20=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image21=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image22=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image23=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    image24=models.ImageField(upload_to="images/nuestros_atletas",blank=True,null=True)
    
    descripcion = CKEditor5Field('Contenido', config_name='default', default='')

    

    def __str__(self):
        return f"Rutina - {self.paquete} - {self.titulo}"

    
    
from django.contrib.auth.models import User

class CompraPaquete(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compras')
    paquete = models.ForeignKey(Paquete, on_delete=models.CASCADE, related_name='compras')
    fecha_compra = models.DateTimeField(auto_now_add=True)
    stripe_payment_intent = models.CharField(max_length=255, blank=True, null=True)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True) 
    entregado = models.BooleanField(default=False) 
    pagado = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Paquetes Vendidos"
        verbose_name_plural = "Paquetes Vendidos"
        unique_together = ('usuario', 'paquete')  # para evitar compras duplicadas

    def __str__(self):
        return f"{self.usuario.username} - {self.paquete.titulo}"



# models.py

from django.contrib.auth.models import User
from django.db import models



from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError

# ------------------------
# Tallas para ropa y calzado
TALLAS_ZAPATO = [
    # Mujer
    {"us": 5, "genero": "mujer", "eu": 35.5, "cm": 22.5},
    {"us": 5.5, "genero": "mujer", "eu": 36, "cm": 23},
    {"us": 6, "genero": "mujer", "eu": 36.5, "cm": 23.5},
    {"us": 6.5, "genero": "mujer", "eu": 37, "cm": 23.8},
    {"us": 7, "genero": "mujer", "eu": 37.5, "cm": 24},
    {"us": 7.5, "genero": "mujer", "eu": 38, "cm": 24.5},
    {"us": 8, "genero": "mujer", "eu": 38.5, "cm": 25},
    {"us": 8.5, "genero": "mujer", "eu": 39, "cm": 25.5},
    {"us": 9, "genero": "mujer", "eu": 40, "cm": 26},
    {"us": 9.5, "genero": "mujer", "eu": 40.5, "cm": 26.5},
    {"us": 10, "genero": "mujer", "eu": 41, "cm": 27},
    {"us": 10.5, "genero": "mujer", "eu": 42, "cm": 27.5},
    {"us": 11, "genero": "mujer", "eu": 42.5, "cm": 28},

    # Hombre
    {"us": 6, "genero": "hombre", "eu": 38.5, "cm": 24.5},
    {"us": 6.5, "genero": "hombre", "eu": 39, "cm": 25},
    {"us": 7, "genero": "hombre", "eu": 40, "cm": 25.5},
    {"us": 7.5, "genero": "hombre", "eu": 40.5, "cm": 26},
    {"us": 8, "genero": "hombre", "eu": 41, "cm": 26.5},
    {"us": 8.5, "genero": "hombre", "eu": 42, "cm": 27},
    {"us": 9, "genero": "hombre", "eu": 42.5, "cm": 27.5},
    {"us": 9.5, "genero": "hombre", "eu": 43, "cm": 28},
    {"us": 10, "genero": "hombre", "eu": 44, "cm": 28.5},
    {"us": 10.5, "genero": "hombre", "eu": 44.5, "cm": 29},
    {"us": 11, "genero": "hombre", "eu": 45, "cm": 29.5},
    {"us": 11.5, "genero": "hombre", "eu": 45.5, "cm": 30},
    {"us": 12, "genero": "hombre", "eu": 46, "cm": 30.5},
]

TALLAS_ROPA_CHOICES = [
    ("S", "S"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
    ("XXL", "XXL"),
]

GENERO_CHOICES = [
    ("hombre", "Hombre"),
    ("mujer", "Mujer"),
    ("unisex", "Unisex"),
]

COLOR_CHOICES = [
    ("negro", "Negro"),
    ("blanco", "Blanco"),
    ("gris", "Gris"),
    ("azul", "Azul"),
    ("rojo", "Rojo"),
    ("verde", "Verde"),
    ("amarillo", "Amarillo"),
    ("rosado", "Rosado"),
    ("morado", "Morado"),
    ("naranja", "Naranja"),
    ("marrón", "Marrón"),
    ("beige", "Beige"),
    ("multicolor", "Multicolor"),
]


class TallaRopa(models.Model):
    codigo = models.CharField(max_length=10, unique=True,help_text="Ej: S, M, L, XL")  
    descripcion = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.codigo
    class Meta:
        verbose_name="Tallas Ropa"
        verbose_name_plural="Tallas Ropa"

class TallaCalzado(models.Model):
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES)
    us = models.DecimalField(max_digits=4, decimal_places=1)
    eu = models.DecimalField(max_digits=4, decimal_places=1)
    cm = models.DecimalField(max_digits=4, decimal_places=1)
    class Meta:
        verbose_name="Tallas Calzado"
        verbose_name_plural="Tallas Calzado"
    def __str__(self):
        return f"US {self.us} / EU {self.eu} / {self.cm} cm - {self.genero}"

# ------------------------
# Producto base (ropa, calzado, etc.)
# ------------------------

class Producto(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=100, choices=[('ropa', 'Ropa'), ('calzado', 'Calzado')])
    marca = models.CharField(max_length=255, blank=True, null=True)
    tiene_envio_gratis = models.BooleanField(default=False)
    precio_envio_sucursal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_envio_domicilio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_envio_express_sucursal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_envio_express_domicilio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_envio_internacional = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    foto1 = models.ImageField(upload_to='productos/', blank=True, null=True)
    foto2 = models.ImageField(upload_to='productos/', blank=True, null=True)
    foto3 = models.ImageField(upload_to='productos/', blank=True, null=True)
    foto4 = models.ImageField(upload_to='productos/', blank=True, null=True)
    foto5 = models.ImageField(upload_to='productos/', blank=True, null=True)
    foto6 = models.ImageField(upload_to='productos/', blank=True, null=True)
    foto7 = models.ImageField(upload_to='productos/', blank=True, null=True)
    foto8 = models.ImageField(upload_to='productos/', blank=True, null=True)
    foto9 = models.ImageField(upload_to='productos/', blank=True, null=True)
    foto10 = models.ImageField(upload_to='productos/', blank=True, null=True)
    class Meta:
        verbose_name="Lista de Ropa y Calzado en Tienda"
        verbose_name_plural="Lista de Ropa y Calzado en Tienda"
    def __str__(self):
        return self.titulo
    
    #ESTO LO HICE PARA PODER QUE SE MUESTRE LA FOTO EN EL ENVIO DEL EMAIL
    def get_foto1_url(self):
        return self.foto1.url if self.foto1 else None

class VarianteProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="variantes")
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES)
    color = models.CharField(max_length=50)

    talla_ropa = models.ForeignKey(TallaRopa, on_delete=models.SET_NULL, null=True, blank=True)
    talla_calzado = models.ForeignKey(TallaCalzado, on_delete=models.SET_NULL, null=True, blank=True)

    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    
    
    def clean(self):
        if self.producto.tipo == 'ropa' and not self.talla_ropa:
            raise ValidationError("La ropa requiere una talla de ropa.")
        if self.producto.tipo == 'calzado' and not self.talla_calzado:
            raise ValidationError("El calzado requiere una talla de calzado.")
        if self.talla_ropa and self.talla_calzado:
            raise ValidationError("No se puede asignar ambas tallas a la vez.")
    class Meta:
        verbose_name="Stock tallas ropa Calzado"
        verbose_name_plural="Stock tallas ropa Calzado"

    def __str__(self):
        talla = self.talla_ropa or self.talla_calzado
        return f"{self.producto.titulo} - {self.genero} - {self.color} - {talla}"

# ------------------------
# Producto existente: suplementos
# ------------------------

class SuplementosYFarmacos(models.Model):
    titulo = models.CharField(max_length=255, blank=True, null=True)
    meta_personal = models.CharField(max_length=100, choices=META_PERSONAL_CHOICES, blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    descripcion = models.TextField(blank=True, null=True)
    marca = models.CharField(max_length=255, blank=True, null=True)
    tipo_de_producto = models.CharField(max_length=255, blank=True, null=True)
    fecha_de_vencimiento = models.CharField(max_length=50, blank=True, null=True)
    stock = models.IntegerField(blank=True, null=True)
    tiene_envio_gratis = models.BooleanField(default=False)
    precio_envio_sucursal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_envio_domicilio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_envio_express_sucursal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_envio_express_domicilio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_envio_internacional = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    foto1 = models.ImageField(upload_to='productos/', blank=True, null=True)
    foto2 = models.ImageField(upload_to='productos/', blank=True, null=True)
    foto3 = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return self.titulo
    
    #ESTO LO HICE PARA PODER QUE SE MUESTRE LA FOTO EN EL ENVIO DEL EMAIL
    def get_foto1_url(self):
        return self.foto1.url if self.foto1 else None

    class Meta:
        verbose_name = "Lista de Productos Generales en Tienda"
        verbose_name_plural = "Lista de Productos Generales en Tienda"

# ------------------------
# Dirección de Envío
# ------------------------
OPCIONES_ENTREGA = [
    ('domicilio', 'Entrega a domicilio'),
    ('domicilio_express', 'Entrega a domicilio (Express)'),
    ('sucursal', 'Retiro en sucursal'),
    ('sucursal_express', 'Retiro en sucursal (Express)'),
]

class DireccionDeEnvio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    direccion = models.CharField(max_length=200, help_text="")
    ciudad = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=20)
    pais = models.CharField(max_length=100,default="México")

    # Usa choices aquí 👇
    opcion_entrega = models.CharField(
        max_length=100,
        choices=OPCIONES_ENTREGA,
        default='domicilio',
        verbose_name='¿Retiro en sucursal o prefieres entrega en casa?'
    )

    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name="Direcciones de Clientes"
        verbose_name_plural="Direcciones de Clientes"
    def __str__(self):
        return f'{self.nombre_completo} - {self.direccion}'






from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from fitapp.models import VarianteProducto, SuplementosYFarmacos  # Ajusta si es necesario

def get_default_content_type():
    return ContentType.objects.get_for_model(SuplementosYFarmacos).id

class CarritoItem(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=get_default_content_type)
    object_id = models.PositiveIntegerField()
    producto = GenericForeignKey('content_type', 'object_id')

    # Campos auxiliares
    talla = models.CharField(max_length=20, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)

    # Relación directa con la variante (si aplica)
    variante = models.ForeignKey(VarianteProducto, on_delete=models.SET_NULL, null=True, blank=True)

    cantidad = models.PositiveIntegerField(default=1)
    agregado = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.variante:
            self.talla = str(self.variante.talla_ropa or self.variante.talla_calzado or '')
            self.color = self.variante.color
        super().save(*args, **kwargs)

    def subtotal(self):
        precio = self.variante.precio if self.variante else self.producto.precio
        return precio * self.cantidad

    @property
    def es_ropa_o_calzado(self):
        from fitapp.models import Producto
        return isinstance(self.producto, Producto) and self.producto.tipo in ['ropa', 'calzado']

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"






# ------------------------
# Compra unificada
# ------------------------

class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    direccion = models.ForeignKey(DireccionDeEnvio, on_delete=models.CASCADE)
    pagado = models.BooleanField(default=False)
    envio_realizado = models.BooleanField(default=False)
    notas_de_envio=models.TextField(verbose_name="Notas de Envio", default="",null=True, blank=True)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    
    #ESTO ES PARA CALCULAR EL TOTAL DEL CARRO
    @property
    def total(self):
        return sum(item.subtotal() for item in self.items.all()) + self.direccion.costo_envio
    
    #ESTO ES PARA QUE CUANDO EL USUARIO HAGA UNA COMPRA SE DESCUENTE DEL STOCK DE CADA ITEM
    def procesar_compra(self):
        for item in self.items.all():
            producto = item.producto
            if hasattr(producto, 'stock') and producto.stock is not None:
                if producto.stock < item.cantidad:
                    raise ValueError(f"Stock insuficiente para {producto}")
                producto.stock -= item.cantidad
                producto.save()
    
    class Meta:
        verbose_name="Productos Vendidos "
        verbose_name_plural="Productos Vendidos"            
    def __str__(self):
        return f"Compra #{self.pk} - {self.usuario.username}"

class CompraItem(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="items")

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    producto = GenericForeignKey('content_type', 'object_id')

    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    #ESTO LO AGREGAMOS PARA PODER MOSTRAR LA TALLA Y COLOR EN LA TEMPLATE DE CONFIRMACION DE COMPRA
    variante = models.ForeignKey(VarianteProducto, on_delete=models.SET_NULL, null=True, blank=True)  

    def subtotal(self):
        return self.precio_unitario * self.cantidad
###########