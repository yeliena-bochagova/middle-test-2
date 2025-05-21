# recipe/views.py
from django.shortcuts import render, get_object_or_404
from .models import Recipe, Category

def main(request):
    # Отримуємо 10 випадкових рецептів
    recipes = Recipe.objects.order_by('?')[:10]
    context = {"recipes": recipes}
    return render(request, "main.html", context)

def category_detail(request, category_id):
    # Переконуємося, що категорія існує
    category = get_object_or_404(Category, id=category_id)
    # Фільтруємо рецепти за категорією
    recipes = Recipe.objects.filter(category=category)
    context = {"recipes": recipes, "category": category}
    return render(request, "category_detail.html", context)
