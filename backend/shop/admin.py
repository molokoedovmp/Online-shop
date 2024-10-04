from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    ordering = ('name',)

    def get_prepopulated_fields(self, request, obj=None):
        """Get the prepopulated fields for the admin form.
        
        Args:
            request (HttpRequest): The current request object.
            obj (Model, optional): The object being edited, or None if creating a new object.
        
        Returns:
            dict: A dictionary mapping field names to sequences of field names to use for prepopulation.
        """        return {
            'slug': ('name',),
        }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand',  'price', "discount",
                    'available', 'created_at', 'updated_at')
    list_filter = ('available', 'created_at', 'updated_at')
    ordering = ('title',)

    def get_prepopulated_fields(self, request, obj=None):
        """Get prepopulated fields for the admin form.
        
        Args:
            self: The instance of the admin class.
            request (HttpRequest): The current request object.
            obj (Model, optional): The object being edited, or None if creating a new object.
        
        Returns:
            dict: A dictionary mapping field names to sequences of field names to use for prepopulation.
        """        return {
            'slug': ('title',),
        }
