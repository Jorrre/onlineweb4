from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView, DeleteView

from apps.dashboard.tools import DashboardPermissionMixin
from apps.gallery.models import ResponsiveImage
from apps.webshop.models import Category, Product

from taggit.models import TaggedItem

import logging

logger = logging.getLogger(__name__)


class Overview(DashboardPermissionMixin, TemplateView):
    template_name = 'webshop/dashboard/index.html'
    permission_required = 'webshop.?'


class Categories(DashboardPermissionMixin, TemplateView):
    model = Category
    template_name = 'webshop/dashboard/categories.html'
    permission_required = 'webshop.change_category'

    def get_context_data(self, *args, **kwargs):
        context = super(Categories, self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.all().prefetch_related('products')
        return context


class CategoryView(DashboardPermissionMixin, DetailView):
    model = Category
    template_name = 'webshop/dashboard/category.html'
    permission_required = 'webshop.view_category'


class CategoryCreate(DashboardPermissionMixin, CreateView):
    model = Category
    fields = ['name', 'slug']
    template_name = 'webshop/dashboard/category_update.html'
    permission_required = 'webshop.add_category'

    def get_object(self, *args, **kwargs):
        # django-guardian hack https://github.com/django-guardian/django-guardian/issues/195
        return None

    def get_success_url(self):
        return reverse('dashboard-webshop:categories')


class CategoryUpdate(DashboardPermissionMixin, UpdateView):
    model = Category
    fields = ['name', 'slug']
    template_name = 'webshop/dashboard/category_update.html'
    context_object_name = 'category'
    permission_required = 'webshop.change_product'

    def get_success_url(self):
        return reverse('dashboard-webshop:category', kwargs={'slug': self.object.slug})


class CategoryDelete(DashboardPermissionMixin, DeleteView):
    model = Category
    template_name = 'webshop/dashboard/delete.html'
    permission_required = 'webshop.delete_category'

    def get_success_url(self):
        return reverse('dashboard-webshop:categories')


class ProductView(DashboardPermissionMixin, DetailView):
    model = Product
    template_name = 'webshop/dashboard/product.html'
    permission_required = 'webshop.view_product'


class ProductCreate(DashboardPermissionMixin, CreateView):
    model = Product
    fields = ['name', 'slug', 'short', 'description', 'price', 'stock']
    template_name = 'webshop/dashboard/product_update.html'
    permission_required = 'webshop.add_product'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductCreate, self).get_context_data(*args, **kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs.get('category_slug'))
        return context

    def form_valid(self, form):
        product = form.save(commit=False)
        # Setting foreign key
        category = get_object_or_404(Category, slug=self.kwargs.get('category_slug'))
        product.category = category
        return super(ProductCreate, self).form_valid(form)

    def get_object(self, *args, **kwargs):
        # django-guardian hack https://github.com/django-guardian/django-guardian/issues/195
        return None

    def get_success_url(self):
        return reverse('dashboard-webshop:category', kwargs={'slug': self.kwargs.get('category_slug')})


class ProductUpdate(DashboardPermissionMixin, UpdateView):
    model = Product
    fields = ['name', 'slug', 'short', 'description', 'price', 'stock']
    template_name = 'webshop/dashboard/product_update.html'
    context_object_name = 'product'
    permission_required = 'webshop.change_product'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductUpdate, self).get_context_data(*args, **kwargs)
        context['category'] = self.object.category
        return context

    def get_success_url(self):
        return reverse('dashboard-webshop:product', kwargs={'slug': self.object.slug})


class ProductDelete(DashboardPermissionMixin, DeleteView):
    model = Product
    template_name = 'webshop/dashboard/delete.html'
    permission_required = 'webshop.delete_product'

    def get_success_url(self):
        return reverse('dashboard-webshop:category', kwargs={'slug': self.object.category.slug})


class ProductImage(DashboardPermissionMixin, DetailView):
    model = Product
    template_name = 'webshop/dashboard/image.html'
    permission_required = 'webshop.change_product'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductImage, self).get_context_data(*args, **kwargs)
        # Filter out potential ResponsiveImage objects that have orphan file references
        images = ResponsiveImage.objects.all().order_by('-timestamp')[:15]
        context['images'] = filter(lambda i: i.file_status_ok(), images)

        context['tags'] = sorted(set(tag.tag.name for tag in TaggedItem.objects.filter(
            content_type=ContentType.objects.get_for_model(ResponsiveImage)
        ).order_by('tag__name')))

        return context

    def post(self, request, *args, **kwargs):
        pass