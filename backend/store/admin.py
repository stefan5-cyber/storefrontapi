from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models


@admin.register(models.Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['description', 'discount']
    list_editable = ['discount']
    ordering = ['discount']


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_field = ['title']

    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist') + '?' + urlencode(
                {
                    'collection__id__exact': str(collection.id)
                }
            )
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        # annotate new field
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )


class ReviewInline(admin.TabularInline):
    model = models.Review
    extra = 0


class ProductInventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<=5', 'Low'),
            ('>5', 'OK')
        ]

    def queryset(self, request, queryset):
        if self.value() == '<5':
            return queryset.filter(inventory__lte=5)
        if self.value() == '>5':
            return queryset.filter(inventory__gt=5)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    inlines = [ReviewInline]
    list_display = [
        'title', 'unit_price',
        'collection_title', 'inventory_status'
    ]
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', ProductInventoryFilter]
    list_select_related = ['collection']
    list_per_page = 15
    autocomplete_field = ['collection']
    ordering = ['title']
    prepopulated_fields = {
        'slug': ['title']
    }

    @admin.display(ordering='collection')
    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        return 'OK' if product.inventory >= 5 else 'Low'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request, f'{updated_count} products was successfully updated'
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page: 15
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = [
        'user__first_name_istartswith',
        'user__last_name_istartswith'
    ]


class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'placed_at',
        'payment_status'
    ]
    inlines = [OrderItemInline]
    ordering = ['placed_at']
    list_prefetch_related = ['customer__user', 'items']

    def payment_status(self, order):
        return order.__str__
