import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Order, OrderItem, ShippingAddress


def export_paid_to_csv(modeladmin, request, queryset):
    """Exports paid queryset objects to a CSV file.
    
    Args:
        modeladmin (admin.ModelAdmin): The ModelAdmin instance.
        request (HttpRequest): The current request object.
        queryset (QuerySet): The queryset of objects to be exported.
    
    Returns:
        HttpResponse: A response object with the CSV file content.
    """
    opts = modeladmin.model._meta
    content_disposition = f"attachment; filename=Paid{opts.verbose_name}.csv"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = content_disposition
    writer = csv.writer(response)
    fields = [
        field
        for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many 
    ]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        if not getattr(obj, "paid"):
            continue
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%d/%m/%Y")
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_paid_to_csv.short_description = "Export Paid to CSV"

def export_not_paid_to_csv(modeladmin, request, queryset):
    """
    Exports unpaid objects from a queryset to a CSV file.
    
    Args:
        modeladmin (admin.ModelAdmin): The ModelAdmin instance.
        request (HttpRequest): The current request.
        queryset (QuerySet): The queryset of objects to be exported.
    
    Returns:
        HttpResponse: A response containing the CSV file for download.
    """
    opts = modeladmin.model._meta
    content_disposition = f"attachment; filename=NotPaid{opts.verbose_name}.csv"
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = content_disposition
    writer = csv.writer(response)
    fields = [
        field
        for field in opts.get_fields()
        if not field.many_to_many and not field.one_to_many 
    ]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        if getattr(obj, "paid"):
            continue
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%d/%m/%Y")
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_not_paid_to_csv.short_description = "Export Not Paid to CSV"

def order_pdf(obj):
    """Generate a PDF link for an order.
    
    Args:
        obj (Order): The order object for which to generate the PDF link.
    
    Returns:
        str: A safe HTML string containing an anchor tag with a link to the order's PDF.
    """
    url = reverse('payment:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')

order_pdf.short_description = 'Invoice'

class ShippingAdressAdmin(admin.ModelAdmin):
    list_display = ('full_name_bold','user', 'email', 'country', 'city', 'zip')
    empty_value_display = "-empty-"
    list_display_links = ('full_name_bold',)
    list_filter = ('user', 'country', 'city')

    @admin.display(description="Full Name", empty_value="Noname")
    def full_name_bold(self, obj):
        """
        Formats the full name of an object in bold HTML.
        
        Args:
            obj (object): The object containing a 'full_name' attribute.
        
        Returns:
            """Get the list of read-only fields for the admin form.
            
            Args:
                request (HttpRequest): The current request object.
                obj (Model, optional): The object being edited. Defaults to None.
            
            Returns:
                list: A list of field names that should be read-only in the admin form.
            """
            SafeString: An HTML-safe string with the full name wrapped in bold tags.
        """
        return format_html("<b style='font-weight: bold;'>{}</b>", obj.full_name)
    
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['price', 'product', "quantity", "user"]
        return super().get_readonly_fields(request, obj)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'shipping_address', 'amount',
                    'created', 'updated', 'paid', 'discount', order_pdf
]
    list_filter = ['paid', 'updated','created',]
    inlines = [OrderItemInline]
    list_per_page = 15
    list_display_links = ['id', 'user']
    actions = [export_paid_to_csv, export_not_paid_to_csv]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress, ShippingAdressAdmin)


