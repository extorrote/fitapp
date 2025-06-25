from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr_name):
    return getattr(obj, attr_name, None)



######## ESTE ES PARA PODER MOSTRAR LO RELACIONADO CON EL PRECIO UNITARIO Y EL TODAL PAGADO EN LA TEMPLATE DE CONFIRMACION

from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
