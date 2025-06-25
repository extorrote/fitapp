from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import RegistroUsuario, META_PERSONAL_CHOICES, GENERO_CHOICES, TIPO_ABORTO_CHOICES,SuplementosYFarmacos




class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,#######ESTE ES PARA LA MERA CONTRASEÑA
        label="Contraseña"
        
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,#############ESTE ES PARA LA CONFIRMACION DE LA CONTRASEÑA
        label="Confirmar Contraseña"
    )

    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name' ,'password']
        labels = {
            'username': 'Nombre de usuario (con este iniciaras sesión)',#######AQUI ESTOY LLAMANDO DEL MODELO USER LA CONTRASEÑA EMAIL Y USERNAME
            'password': 'Contraseña',
             'first_name':'Tu Nombre',
            'last_name':'Apellidos',
            'email':'Correo Electronico',
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('confirm_password'):
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash the password
        user.email = self.cleaned_data["email"]  # Ensure email is set
        if commit:
            user.save()
        return user


from .labels import labels

class RegistroMujerForm(forms.ModelForm):
    class Meta:
        model = RegistroUsuario##AQUI PARA QUE SE REGISTRE UN DUEÑO DE NEGOCIO ESTAMOS PIDIENDO ESTOS DATOS
        fields = '__all__'
        labels = labels






from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserEditForm(forms.ModelForm):
    current_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Contraseña actual",
        required=False
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Nueva contraseña",
        required=False
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirmar nueva contraseña",
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        labels = {
            'username': 'Nombre de usuario',
            'password': 'Nueva contraseña',
            'first_name': 'Tu Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo Electrónico',
        }

    def __init__(self, *args, **kwargs):
        # Accept and store the user instance to validate the current password
        self.user_instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password or confirm_password:
            # Require current password if changing password
            if not current_password:
                raise ValidationError("Debes ingresar tu contraseña actual para cambiarla.")

            if not self.user_instance.check_password(current_password):
                raise ValidationError("La contraseña actual es incorrecta.")

            if new_password != confirm_password:
                raise ValidationError("Las nuevas contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("password")

        if new_password:
            user.set_password(new_password)
        else:
            # Keep the existing password hash
            existing = User.objects.get(pk=user.pk)
            user.password = existing.password

        if commit:
            user.save()
        return user



from .models import NuestrosAtletas

class AtletaForm(forms.ModelForm):
    class Meta:
        model = NuestrosAtletas
        fields= '__all__'
        labels={
            'nombre':'Nombre','edad':'Edad','titulos_competitivos':'Titulos Competitivos'
            
        }
        
        
        

from django import forms
from .models import Paquete, ContenidoDieta, ContenidoRutina

class PaqueteForm(forms.ModelForm):
    class Meta:
        model = Paquete
        fields = ['meta_personal','titulo','image1','categoria', 'descripcion','es_premium', 'precio']


from django_ckeditor_5.fields import CKEditor5Field

class ContenidoDietaForm(forms.ModelForm):
    descripcion = CKEditor5Field(config_name='default')
    class Meta:
        model = ContenidoDieta
        fields = '__all__'


class ContenidoRutinaForm(forms.ModelForm):
    descripcion = CKEditor5Field(config_name='default')
    class Meta:
        model = ContenidoRutina
        fields = '__all__'





from .models import SuplementosYFarmacos

class SuplementosYFarmacosForm(forms.ModelForm):
    class Meta:
        model = SuplementosYFarmacos
        fields = [
            'meta_personal', 'titulo', 'precio',  'descripcion',
            'marca', 'tipo_de_producto', 'fecha_de_vencimiento', 'stock',
            'foto1', 'foto2', 'foto3'
        ]


from django import forms
from .models import DireccionDeEnvio

class DireccionDeEnvioForm(forms.ModelForm):
    class Meta:
        model = DireccionDeEnvio
        fields = ['nombre_completo', 'telefono', 'direccion', 'ciudad', 'estado', 'codigo_postal', 'pais', 'opcion_entrega']
        labels = {
            'opcion_entrega': '¿Retiro en sucursal o prefieres entrega en casa?(El valor del envío se ajusta según tu elección)',
            'direccion':'Calle y Numero'
        }


from django.core.validators import RegexValidator
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()    
    phone = forms.CharField(
        max_length=15, 
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$', 
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )]
    )
    message = forms.CharField(widget=forms.Textarea)