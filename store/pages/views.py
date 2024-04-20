from django.shortcuts import render
from django.views.generic import TemplateView
from datetime import datetime, timedelta
from django.db.models import Count, Q, F

from store.products.models import Product


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        products = Product.objects.active_with_stock_info()

        last_week = datetime.today() - timedelta(days=7)
        most_sold_products = products.filter(sale_records__sold_at__gt=last_week)
        most_sold_products = most_sold_products.annotate(num_sold=F('sale_records__num_sold'))
        most_sold_products = most_sold_products.order_by('-num_sold', '-created')[:5]

        last_month = datetime.today() - timedelta(days=30)
        most_hits_products = products.annotate(count=Count('hits', filter=Q(producthit__created__gt=last_month)))
        most_hits_products = most_hits_products.order_by('-count', '-created')

        context['most_sold_products'] = most_sold_products
        context['most_hits_products'] = most_hits_products
        return context
    

class HelpPageView(TemplateView):
    template_name = 'help.html'
