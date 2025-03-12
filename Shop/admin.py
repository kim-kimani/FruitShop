from django.contrib import admin
from django import forms
from .models import Product, Category, SubCategory, ProductImage
# Register your models here.

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sub_category'].queryset = SubCategory.objects.none()
        
        if 'category' in self.fields:
            try:
                category_id = int(self.data.get("category"))
                self.fields["sub_category"].queryset = SubCategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        
        elif self.isinstance.pk:
            self.fields["sub_category"].queryset = self.instance.category.subcategories.all()
    
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'truncated_description', 'category', 'sub_category')
    list_filter = ('price',)
    inlines = [ProductImageInline]
    
    def truncated_description(self, obj):
        max_length = 80
        if len(obj.description) > max_length:
            return obj.description[:max_length] + '...'
        return obj.description
    truncated_description.short_description = 'Description'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory)

