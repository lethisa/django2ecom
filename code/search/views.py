
from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product

# Create your views here.

class SearchProductView(ListView):
    template_name = "search/view.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        query = self.request.GET.get('q')
        context['query'] = query
        # SearchQuery.objects.create(query=query)
        return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        # print(request.GET)
        method_dict = request.GET
        # query = request.GET.get('q')
        query = method_dict.get('q', None)
        if query is not None:
            # lookups = Q(title__icontains=query) | Q(description__icontains=query)
            return Product.objects.search(query)
        else:
            return Product.objects.featured()

    """
    __icontains = field contains this
    __iexact = field is exactly this
    """
