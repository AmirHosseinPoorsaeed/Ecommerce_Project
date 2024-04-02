from django import template

register = template.Library()


arabic = '۰١٢٣٤٥٦٧٨٩'
english = '0123456789'


@register.filter(name='persian_number')
def convert_to_persian(value):
    value = str(value)
    translation_table = str.maketrans(english, arabic)
    return value.translate(translation_table)
