from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required







#class CategoryList(ListView):
 #   # Указываем модель, объекты которой мы будем выводить
 #   model = Category
    # Поле, которое будет использоваться для сортировки объектов
    #ordering = 'title'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
   # template_name = 'categorys.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
   # context_object_name = 'categorys'

#class CategoryDetail(ListView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    #model = Category
    # Используем другой шаблон — product.html
    #template_name = 'category.html'
    # Название объекта, в котором будет выбранный пользователем продукт
   # context_object_name = 'category'

class PostList(ListView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post # не моуг понять почему при вставке заместо модел queryset = Post.objects.order_by('-publication_date')
    #не определяется обьект, по коду из технической документации с помощью этой строчки можно фильтровать дату публикации
    ordering = 'header'
    # Используем другой шаблон — product.html
    template_name = 'posts.html'
    # фильтрует буликации по дате создания
    #queryset = Post.objects.order_by('-time_in')
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'posts'

    paginate_by = 2 # вот так мы можем указать количество записей на странице

    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['filterset'] = self.filterset
        return context




class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    # Используем другой шаблон — product.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
        # К словарю добавим текущую дату в ключ 'time_now'.
        context['time_now'] = datetime.utcnow()
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_post'] = None
        return context

    #def create_post(request):
       # form = PostForm()
        #return render(request, 'post_edit.html', {'form': form})

class PostCreate(CreateView):
     #Указываем нашу разработанную форму
    form_class = PostForm
     #модель товаров
    model = Post
     #и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'

# Добавляем представление для изменения товара.
class PostUpdate(UpdateView):
    # Указываем нашу разработанную форму
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'

# Представление удаляющее товар.
class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'login.html'



class ProtectedView(LoginRequiredMixin, TemplateView):
    template_name = 'prodected_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/posts/')
