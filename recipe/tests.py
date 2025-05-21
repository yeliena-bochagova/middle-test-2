from django.test import TestCase
from django.urls import reverse
from .models import Recipe, Category

class RecipeViewsRandomTest(TestCase):
    def setUp(self):
        # Створимо категорію і достатню кількість рецептів для тестування випадковості
        self.category = Category.objects.create(name="Сніданки")
        # Створимо, наприклад, 25 рецептів. Якщо їх більше за 10, шанс отримати різні 10 при повторних запитах високий.
        for i in range(25):
            Recipe.objects.create(
                title=f"Рецепт {i}",
                description=f"Опис рецепту {i}",
                instructions="Спосіб приготування",
                ingredients="Інгредієнти",
                category=self.category,
            )

    def test_main_view_returns_exactly_10_recipes(self):
        response = self.client.get(reverse("main"))
        self.assertEqual(response.status_code, 200)
        # Переконуємось, що в контексті міститься змінна 'recipes'
        self.assertIn("recipes", response.context)
        # Перевіряємо, що завжди повертається рівно 10 рецептів
        self.assertEqual(len(response.context["recipes"]), 10)

    def test_main_view_randomness(self):
        """
        Тест для перевірки випадковості.
        """
        response1 = self.client.get(reverse("main"))
        recipes1 = list(response1.context["recipes"].values_list('id', flat=True))
        response2 = self.client.get(reverse("main"))
        recipes2 = list(response2.context["recipes"].values_list('id', flat=True))

        self.assertEqual(len(recipes1), 10)
        self.assertEqual(len(recipes2), 10)
        # Якщо база містить більше 10 рецептів, з великою ймовірністю, порядок має відрізнятися.
        self.assertNotEqual(recipes1, recipes2, "Два послідовних запити повернули однаковий набір рецептів. Це може бути випадковістю.")


class RecipeViewsCategoryDetailTest(TestCase):
    def setUp(self):
        # Створення категорій та рецептів
        self.category = Category.objects.create(name="Обіди")
        self.other_category = Category.objects.create(name="Вечері")
        # Для категорії "Обіди" створимо 15 рецептів.
        for i in range(15):
            Recipe.objects.create(
                title=f"Обідний рецепт {i}",
                description=f"Опис обідного рецепту {i}",
                instructions="Інструкції",
                ingredients="Інгредієнти",
                category=self.category,
            )
        # Для іншої категорії створимо декілька рецептів (для перевірки відсіювання)
        for i in range(5):
            Recipe.objects.create(
                title=f"Вечірній рецепт {i}",
                description=f"Опис вечірнього рецепту {i}",
                instructions="Інструкції",
                ingredients="Інгредієнти",
                category=self.other_category,
            )

    def test_category_detail_returns_all_recipes_of_category(self):
        response = self.client.get(reverse("category_detail", args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "category_detail.html")
        self.assertIn("recipes", response.context)
        # Оскільки для категорії створено 15 рецептів, перевіряємо, що їх повертається саме 15.
        self.assertEqual(len(response.context["recipes"]), 15)

    def test_category_detail_only_for_specified_category(self):
        response = self.client.get(reverse("category_detail", args=[self.other_category.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "category_detail.html")
        self.assertIn("recipes", response.context)
        # Для іншої категорії має повернутися 5 рецептів
        self.assertEqual(len(response.context["recipes"]), 5)
