from django.contrib import admin
from django import forms
from .models import Clients, Features, ProductArea


class ClientsModelForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = '__all__'


class ClientsAdmin(admin.ModelAdmin):
    form = ClientsModelForm
    # list_display = ('title', 'published_date', 'news_paper')
    # list_filter = ['published_date']
    search_fields = ['name']


class ProductAreaModelForm(forms.ModelForm):
    class Meta:
        model = ProductArea
        fields = '__all__'


class ProductAreaAdmin(admin.ModelAdmin):
    form = ProductAreaModelForm
    search_fields = ['name']


class FeaturesModelForm(forms.ModelForm):
    class Meta:
        model = ProductArea
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 10}),
            'priority': forms.NumberInput(attrs={'max_length': '3'}),
        }


class FeaturesAdmin(admin.ModelAdmin):
    form = FeaturesModelForm
    list_display = ('title', 'client', 'priority', 'product_area', 'target_date', 'status')
    search_fields = ['name']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # This is the case when obj is already created i.e. it's an edit
            return ['client']
        else:
            return []


admin.site.register(Clients)
admin.site.register(ProductArea, ProductAreaAdmin)
admin.site.register(Features, FeaturesAdmin)
