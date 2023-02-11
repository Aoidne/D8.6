from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse




class Author(models.Model):
    author_name = models.CharField(max_length=128)
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)# из фала users берем абстракт юзера

    def __str__(self):
        return f'id={self.id}, user={self.user}, author_name="{self.author_name}", rating={self.rating}'

    def some_view(request):
        current_user = request.user
        if current_user.is_authenticated:
            print('You are authenticated')
        else:
            print('You are not authenticated')






    #def update_rating(self):
     # немножко не понял как делать


class Category(models.Model):
    name = models.CharField(unique=True,max_length=255)
    #texting = models.CharField(max_length=255) #описание категории о чем оно

    def __str__(self):
        return self.name.title()




POSITIONS = [
    ('0', 'Статья'),
    ('1', 'Новости'),
]

class Post(models.Model):
    field = models.CharField(max_length=1, choices=POSITIONS, default='0') # статья или новость, берем данные из файла data
    time_in = models.DateTimeField(auto_now_add=True) # дата и время создания
    published = models.DateTimeField(null=True, blank=True)
    header = models.CharField(max_length=255) # заголовок статьи новости
    text = models.TextField(unique=True) # так как тексты могут быть большие берем TextField
    rating = models.IntegerField(default=0) # рейтинг новости или статьи, флоат
    category = models.ForeignKey('Category', related_name='posts',on_delete=models.CASCADE)# тут остается сделать свзяь многие ко многим с моделью категории
    posts = models.ForeignKey(Author,null=True, blank=True, on_delete=models.CASCADE)  # связь один ко многим с автором
    #def publish(self):
        #self.published = timezone.now()
        #self.save() не понимаю почему save показывает ошиюку

    def __str__(self):
        return self.field.pop()

    def __str__(self):
        return f'{self.category.title()}:{self.header.title()} '

    def like(self):
        self.rating += 1

    def dislike(self):
        self.rating -= 1

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])





class PostCategory(models.Model):
    post = models.ForeignKey(Post,null=True,blank=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)




class Comment(models.Model):
    text_comment = models.TextField(max_length=255) #текст комментария
    time_in = models.DateTimeField(auto_now_add=True) # время когда создали комментарий
    rating = models.FloatField(default=0.0) # рейтинг комментария
    comments = models.ForeignKey(Post,related_name="comment", null=True, on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)

