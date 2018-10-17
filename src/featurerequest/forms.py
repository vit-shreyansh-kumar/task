from django import forms
import datetime

from .models import Features


class FeatureForm(forms.ModelForm):
    class Meta:
        model = Features
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'max_length': '100'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.NumberInput(attrs={'class': 'form-control'}),
            'target_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'product_area': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),

        }

    def clean(self):
        target_date = self.cleaned_data['target_date']
        status = self.cleaned_data['status']
        if status == 'A' and target_date < datetime.date.today():
            self.add_error('target_date', 'Active Feature Request can not have a past Target date.')
        super().clean()


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=150)
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}), min_length=8)
