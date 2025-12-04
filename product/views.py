
from django.views.generic import DetailView,TemplateView
from product.models import Product,Category


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'


class NavBarPartialView(TemplateView):
    template_name = 'includes/navbar.html'

    def get_context_data(self, **kwargs):
        context = super(NavBarPartialView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class CategoryStyle(TemplateView):
    template_name = 'category.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryStyle, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductsListView(TemplateView):
    template_name = 'product/products_list.html'
    queryset = Product.objects.all()


    def get_context_data(self, **kwargs):
        request = self.request
        print(request.GET)

        colors = request.GET.getlist('color')
        sizes = request.GET.getlist('size')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        queryset = Product.objects.all()
        if colors:
            queryset = queryset.filter(color__title__in=colors).distinct()
        if sizes:
            queryset = queryset.filter(size__title__in=sizes)
        if min_price and max_price:
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['object_list'] = queryset
        return context
