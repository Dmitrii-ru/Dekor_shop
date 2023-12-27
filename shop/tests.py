from django.test import TestCase
from django.urls import reverse
from .cache import get_test_data



class CategoryListTestCase(TestCase):
    def setUp(self):
        self.categories = get_test_data(model=None)
        print(self.categories)
        # Создайте тестовые данные, включая объекты Category
        pass

    def test_reverse_categories(self):

        for category in self.categories:
            self.assertEqual(
                self.client.get(reverse('shop:groups', kwargs={'slug_category': category.slug})),
                200
            )

