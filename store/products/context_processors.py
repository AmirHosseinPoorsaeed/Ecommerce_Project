from .models import Category


def categories(request):
    return {'categories': Category.get_annotated_list()}
