from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Property, Investment, Crop
from .utilities import export_to_csv, export_to_json

class InvestmentInline(admin.StackedInline):
    model = Investment
    extra = 1

class UserAdmin(BaseUserAdmin):
    inlines = (InvestmentInline,)
    actions = ['export_json', 'export_csv']

    def export_json(self, request, queryset):
        return export_to_json(self, request, queryset.filter(groups__name='Investor'))
    export_json.short_description = "Export selected investors to JSON"

    def export_csv(self, request, queryset):
        return export_to_csv(self, request, queryset.filter(groups__name='Investor'))
    export_csv.short_description = "Export selected investors to CSV"

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_type', 'title', 'description', 'location', 'area', 'price')
    list_per_page = 10
    search_fields = ('title', 'property_type')
    list_filter = ('property_type','location')
    ordering = ('title',)

class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('property', 'investor', 'amount', 'date')
    list_per_page = 10
    search_fields = ('property__title', 'investor__username')
    list_filter = ('property', 'investor',)
    ordering = ('date',)

class CropAdmin(admin.ModelAdmin):
    list_display = ('property', 'name', 'yield_per_hectare')
    list_per_page = 10
    search_fields = ('property__title', 'name')
    list_filter = ('property',)
    ordering = ('name',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Investment, InvestmentAdmin)
admin.site.register(Crop, CropAdmin)
