from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .permission import upload_catalog_permission
from .models import *

from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank

paginate_num = 35


def index(request):
    """
    Start page
    """

    print(Category._meta.get_field('name').unique)
    return render(request, 'shop/index.html')


"""
Category
"""


class CategoryList(ListView):
    """
    CategoryList
    """
    model = Category
    context_object_name = 'categories'
    paginate_by = paginate_num
    queryset = Category.objects.filter(is_active=True).values('site_name', 'slug')


"""
Group
"""


class GroupList(ListView):
    """
    GroupList
    """
    model = Group
    context_object_name = 'groups'
    paginate_by = paginate_num

    def get_queryset(self):
        queryset = Group.objects.only(
            'site_name', 'slug').filter(is_active=True, category__slug=self.kwargs['slug_category'])
        # queryset = cache_filter_model(Group, {'category__slug': self.kwargs['slug_category'], })
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GroupList, self).get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category.objects.only('site_name', 'slug'),
            slug=self.kwargs['slug_category']
        )

        return context


"""
Product
"""


class ProductsList(ListView):
    """
    ProductsList
    """
    model = Product
    context_object_name = 'products'
    paginate_by = paginate_num
    queryset = None

    def get_queryset(self):
        queryset = Product.objects.select_related(
            'promo_group',
        ).only(
            'slug', 'site_name', 'price', 'old_price', 'image', 'promo_group'
        ).filter(
            is_active=True,
            group__slug=self.kwargs['slug_group'],
            group__category__slug=self.kwargs['slug_category'],
        )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsList, self).get_context_data(**kwargs)
        category = get_object_or_404(Category.objects.only('site_name', 'slug'), slug=self.kwargs['slug_category'])
        group = get_object_or_404(Group.objects.only('site_name', 'slug'), slug=self.kwargs['slug_group'])
        context.update({'category': category, 'group': group})
        return context


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    queryset = None

    def get_object(self, queryset=None):
        f = ['group__category__slug',
             'group__category__site_name',
             'group__slug',
             'group__site_name',
             ] + [f.name for f in Product._meta.fields]

        obj = get_object_or_404(
            Product.objects.only(*f).select_related(
                'group__category'
            ).prefetch_related(
                'gallery_img_product'
            ),
            slug=self.kwargs['slug'],
            group__slug=self.kwargs['slug_group'],
            group__category__slug=self.kwargs['slug_category'],
            is_active=True
        )

        return obj


class SearchProduct(ListView):
    paginate_by = paginate_num
    context_object_name = "products"
    template_name = "shop/search.html"

    def get_queryset(self):
        query = self.request.GET.get("p", None)
        if query:
            search_vector = SearchVector("sv_site_name")
            search_query = SearchQuery(query)
            results = Product.objects.only(
                'group__category__slug', 'group__slug', 'slug', 'site_name', 'price', 'old_price', 'image',
                'promo_group'
            ).select_related(
                'group__category', 'promo_group'
            ).annotate(rank=SearchRank(
                search_vector, search_query, weights=[0.2, 0.4, 0.6, 0.8]
            )).filter(
                rank__gt=0.1, rank__lt=0.4, is_active=True
            ).order_by("-rank")
            return results
        else:
            return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['p'] = self.request.GET.get('p', None)
        return context


class PromoProductList(ListView):
    model = Product
    template_name = 'shop/promo.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.only(
            'group__category__slug', 'group__slug', 'slug', 'site_name', 'price', 'old_price', 'image',
        ).select_related(
            'group__category'
        ).filter(
            promo_group__isnull=False, is_active=True
        )
        return queryset
