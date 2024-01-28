from django.shortcuts import get_object_or_404
from pytils.translit import slugify
from django.urls import reverse
from django.db import models
from PIL import Image
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from site_tools.utils.catalog.base_form_string import get_base_form_words
from decimal import Decimal

STOCK_CHOICES = (
    (1, "В наличии"),
    (0, "Под заказ"),
)


class Category(models.Model):
    name = models.TextField('Название по каталогу', unique=True, null=False, blank=False)
    site_name = models.TextField('Название для сайта', blank=False, null=False)
    slug = models.SlugField(
        'Идентификатор в url адресе',
        blank=False,
        max_length=100,
        unique=True
    )
    art = models.CharField("Артикул", max_length=100, blank=False, unique=True)
    image = models.ImageField('Фото в карточку', upload_to='image_card', blank=True)
    is_active = models.BooleanField('Доступен', default=True)

    class Meta:
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + slugify(self.art)
        super(Category, self).save(*args, **kwargs)

    def is_active_true(self):
        self.is_active = True
        self.save()

    def get_absolute_url(self):
        return reverse('shop:groups', kwargs={'slug_category': self.slug})


class Group(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        verbose_name='Принадлежность к категории',
        related_name='group'
    )
    name = models.TextField('Название по каталогу', unique=True, null=False)
    site_name = models.TextField('Название для сайта', blank=False, null=True, unique=True)
    slug = models.SlugField(
        'Идентификатор в url адресе',
        blank=False,
        max_length=100,
        unique=True
    )
    art = models.CharField("Артикул", max_length=100, blank=False, null=True, unique=True)
    image = models.ImageField('Фото в карточку', upload_to='image_card', blank=True)
    is_active = models.BooleanField('Доступен', default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + slugify(self.art)
        super(Group, self).save(*args, **kwargs)

    def is_active_true(self):
        self.is_active = True
        self.save()

    class Meta:
        verbose_name = 'Группа товаров'
        verbose_name_plural = 'Группы товаров'

    def get_absolute_url(self):
        group = get_object_or_404(
            Group.objects.select_related(
                'category'
            ).only('category_slug', 'slug'), pk=self.pk)

        return reverse(
            'shop:products',
            kwargs={
                'slug_category': group.category.slug,
                'slug_group': self.slug}
        )

    def __str__(self):
        return f'{self.name}'


# {'пог. м', 'шт', 'компл', 'упак', 'пар', 'м', 'м2'}
class Product(models.Model):
    STOCK_CHOICES = (
        (1, "В наличии"),
        (0, "Под заказ"),
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name='Принадлежность к группе',
        related_name='product'
    )
    name = models.TextField('Название по каталогу', blank=False, null=False, unique=True)
    site_name = models.TextField(
        'Название для сайта',
        db_index=True,
        blank=False,
        null=True,
        unique=True
    )
    art = models.CharField("Номенклатура.Код", max_length=100, unique=True)
    slug = models.SlugField('Идентификатор в url адресе', blank=False, max_length=100, unique=True)
    unit = models.CharField('Ед. изм.', max_length=20, blank=False, null=False)
    price = models.DecimalField(
        'Цена ',
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        blank=False,
        null=False
    )
    old_price = models.DecimalField(
        'Старая цена',
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        blank=True
    )

    stock = models.IntegerField('Наличие', choices=STOCK_CHOICES, blank=False, null=True, default=1)
    image = models.ImageField(
        'Фото в карточку',
        upload_to='image_card',
        blank=True,
        default='image_default/default.png'
    )
    sv_site_name = SearchVectorField('Триггеры поиска', null=True, blank=True)
    promo_group = models.ForeignKey(
        'PromoProductGroup',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Выбрать акцию'
    )
    is_active = models.BooleanField('Доступен', default=True)

    class Meta:
        verbose_name = 'Карточка товара'
        verbose_name_plural = 'Карточки товаров'
        indexes = [GinIndex(fields=["sv_site_name"])]

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name) + slugify(self.art)

        if self.pk:
            instance = self.__class__.objects.get(id=self.pk)
            if instance.site_name != self.site_name:
                self.sv_site_name = get_base_form_words(self.site_name)
        else:
            self.sv_site_name = get_base_form_words(self.site_name)

        if self.image:
            img = Image.open(self.image.path)
            min_size = min(img.width, img.height)
            left = (img.width - min_size) / 2
            top = (img.height - min_size) / 2
            right = (img.width + min_size) / 2
            bottom = (img.height + min_size) / 2
            img = img.crop((left, top, right, bottom))
            img.thumbnail((638, 638))
            img.save(self.image.path)

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f' {self.art} - {self.name}'

    def get_absolute_url(self):
        product = get_object_or_404(
            Product.objects.select_related(
                'group__category'
            ).only(
                'slug',
                'group__slug',
                'group__category__slug'
            ),
            pk=self.pk
        )

        return reverse(
            'shop:product',
            kwargs={
                'slug_category': product.group.category.slug,
                'slug_group': product.group.slug,
                'slug': self.slug
            }
        )


class ImagesProductsShop(models.Model):
    product = models.ForeignKey(
        Product,
        default='image_default/default.png',
        on_delete=models.CASCADE,
        related_name='gallery_img_product'
    )
    image = models.ImageField(upload_to='image', blank=True)

    class Meta:
        verbose_name = 'Фото галерея'
        verbose_name_plural = 'Фото галерея'


class PromoProductGroup(models.Model):
    name = models.CharField('Название акции', max_length=50, blank=False)
    create_at = models.DateTimeField('Дата создания', auto_now_add=True)
    end_date = models.DateTimeField('Дата окончания акции', blank=False)

    def __str__(self):
        return self.name



    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

#
