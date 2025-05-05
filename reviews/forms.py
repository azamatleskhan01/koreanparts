from django import forms
from .models import Category

class AutoPartSearchForm(forms.Form):
    search = forms.CharField(
        label='Поиск',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Введите название запчасти'}),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label='Категория',
        empty_label="Все категории",
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    min_price = forms.DecimalField(
        label='Минимальная цена',
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Мин. цена', 'step': '0.01'}),
    )
    max_price = forms.DecimalField(
        label='Максимальная цена',
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Макс. цена', 'step': '0.01'}),
    )


from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    """Форма для добавления отзыва с фото."""
    class Meta:
        model = Review
        fields = ["rating", "comment", "image"]
        widgets = {
            "rating": forms.Select(choices=[(i, str(i)) for i in range(1, 6)]),
            "comment": forms.Textarea(attrs={"rows": 4, "placeholder": "Оставьте ваш отзыв..."})
        }

