from django_filters import FilterSet, ModelChoiceFilter
from .models import Post, Category


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.

class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='postcategory__category', # требуется для того чтобы сделать свою фильтраци с изменением названия
        queryset=Category.objects.all(),
        label='Category',
        empty_label='любая'
    )

    class Meta:
# В Meta классе мы должны указать Django модель,
# в которой будем фильтровать записи.
        model = Post
# В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
        fields = {
            'header': ['icontains'],
            'rating': ['icontains'],
        }
