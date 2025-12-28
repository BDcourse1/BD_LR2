from django.db import models
# Импорт для работы с ошибками валидации
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.core.validators import MinValueValidator, MaxValueValidator


# ----------------------------------------------------------------------
# 📌 1. ПОЛЬЗОВАТЕЛЬСКИЙ ВАЛИДАТОР (НА УРОВНЕ ПОЛЯ)
# ----------------------------------------------------------------------

def validate_positive_price(value):
    """
    Проверяет, что цена является неотрицательным числом.
    """
    if value < 0:
        # Возбуждаем исключение ValidationError
        raise ValidationError(
            'Цена (%(value)s) не может быть отрицательной.',
            code='negative_price',
            params={'value': value},
        )


# ====================================================================
# I. Связь «Один-ко-Многим» (One-to-Many)
# ====================================================================

class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True,
                            verbose_name='Название')

    description = models.TextField(null=True, blank=True, verbose_name='Описание рубрики')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']


class Bb(models.Model):
    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(verbose_name='Описание')

    # 📌 ПРИМЕНЕНИЕ ВАЛИДАТОРА: добавляем validators=[validate_positive_price]
    price = models.FloatField(verbose_name='Цена', validators=[validate_positive_price])

    published = models.DateTimeField(auto_now_add=True, db_index=True,
                                     verbose_name='Опубликовано')

    # 1. ForeignKey
    rubric = models.ForeignKey('Rubric', null=True,
                               on_delete=models.PROTECT, verbose_name='Рубрика')

    # 2. ManyToManyField
    tags = models.ManyToManyField('Tag', verbose_name='Теги', related_name='boards')

    # 3. ManyToManyField с 'through'
    rated_by = models.ManyToManyField(
        'ProjectUser',
        through='BbRating',
        verbose_name='Оценившие пользователи',
        related_name='rated_boards'
    )

    # 📌 2. ВАЛИДАЦИЯ МОДЕЛИ: метод clean()
    def clean(self):
        errors = {}

        # Проверка на "Прошлогодний снег"
        if self.title == 'Прошлогодний снег':
            # Привязываем ошибку к полю title (в вашем примере привязка была к content)
            errors['title'] = ValidationError('Такой товар не продается.', code='bad_item')

            # Если есть ошибки, возбуждаем исключение
        if errors:
            raise ValidationError(errors)

    # 📌 ИСПРАВЛЕНИЕ АДМИН-ПАНЕЛИ
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published']


# ====================================================================
# II. Связь «Один-к-Одному» (One-to-One)
# ====================================================================

class BbDetail(models.Model):
    bb = models.OneToOneField(
        Bb,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name='Объявление'
    )
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров')

    # 📌 ИСПРАВЛЕНИЕ АДМИН-ПАНЕЛИ
    def __str__(self):
        return f"Детали для: {self.bb.title}"

    class Meta:
        verbose_name_plural = 'Детали объявлений'
        verbose_name = 'Деталь объявления'


# ====================================================================
# III. Связь «Многие-ко-Многим» (Many-to-Many)
# ====================================================================

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Тег')

    color = models.CharField(max_length=7, default='#ffffff', verbose_name='Цвет тега')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Теги'
        verbose_name = 'Тег'


class ProjectUser(models.Model):
    username = models.CharField(max_length=50, unique=True, verbose_name='Имя пользователя')

    registration_date = models.DateField(auto_now_add=True, null=True, verbose_name='Дата регистрации')

    # 📌 ИСПРАВЛЕНИЕ АДМИН-ПАНЕЛИ
    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = 'Пользователи проекта'
        verbose_name = 'Пользователь проекта'


class BbRating(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, verbose_name='Объявление')
    user = models.ForeignKey(ProjectUser, on_delete=models.CASCADE, verbose_name='Пользователь')

    # Добавляем валидаторы: минимум 1, максимум 5
    rating_value = models.IntegerField(
        verbose_name='Оценка (1-5)',
        validators=[
            MinValueValidator(1, message="Оценка не может быть меньше 1"),
            MaxValueValidator(5, message="Оценка не может быть больше 5")
        ]
    )
    rated_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата оценки')

    def __str__(self):
        return f"Оценка {self.rating_value}/5 для '{self.bb.title}' от {self.user.username}"

    class Meta:
        verbose_name_plural = 'Оценки объявлений'
        verbose_name = 'Оценка объявления'
        unique_together = ('bb', 'user')



class BbImage(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='bbs/images/', verbose_name='Изображение')
    description = models.CharField(max_length=100, blank=True, verbose_name='Описание фото')

class BbFeature(models.Model):
    bb = models.ForeignKey(Bb, on_delete=models.CASCADE, related_name='features', verbose_name='Объявление')
    name = models.CharField(max_length=50, verbose_name='Параметр')
    value = models.CharField(max_length=100, verbose_name='Значение')

    # ДОБАВЬТЕ ЭТОТ МЕТОД:
    def __str__(self):
        return f"{self.name}: {self.value}"

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'