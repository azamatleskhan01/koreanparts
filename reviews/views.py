from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import AutoPartSearchForm, ReviewForm
from .models import AutoPart


# Главная страница
def home(request):
    return render(request, "Base.html")

# Просмотр каталога запчастей
def catalog_view(request):
    return render(request, 'auto_parts/Allparts.html')  # Убедитесь, что файл 'Allparts.html' существует в папке templates

# Просмотр корзины
def cart_view(request):
    return render(request, 'auto_parts/cart.html')

# Поиск запчастей
def search_view(request):
    form = AutoPartSearchForm(request.GET)
    parts = AutoPart.objects.all()  # Начинаем с всех запчастей

    if form.is_valid():
        # Получаем данные из формы
        search_query = form.cleaned_data.get('search')
        category = form.cleaned_data.get('category')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')

        # Фильтрация по запросу
        if search_query:
            parts = parts.filter(name__icontains=search_query)

        # Фильтрация по категории
        if category:
            parts = parts.filter(category=category)

        # Фильтрация по минимальной цене
        if min_price is not None:
            parts = parts.filter(price__gte=min_price)

        # Фильтрация по максимальной цене
        if max_price is not None:
            parts = parts.filter(price__lte=max_price)

    return render(request, 'auto_parts/search_results.html', {
        'form': form,
        'results': parts
    })

# Добавление отзыва к запчасти
@login_required
def add_review(request, part_id):
    auto_part = get_object_or_404(AutoPart, id=part_id)

    if request.method == "POST":
        form = ReviewForm(request.POST, request.FILES)  # Обрабатываем форму с файлом
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.auto_part = auto_part
            review.save()
            return redirect('part_detail', part_id=part_id)  # Возвращаемся на страницу с деталями запчасти

    else:
        form = ReviewForm()

    return render(request, "auto_parts/add_review.html", {"form": form, "auto_part": auto_part})

def part_detail(request, part_id):
    part = get_object_or_404(AutoPart, id=part_id)
    reviews = part.reviews.all()  # Получаем отзывы для данной детали
    return render(request, 'auto_parts/part_detail.html', {'part': part, 'reviews': reviews})

#####################################################################################
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def test_upload(request):
    # Пример загружаемого файла
    file_name = "test_file.txt"
    file_content = "This is a test file to check MinIO integration."

    # Загружаем файл в MinIO
    path = default_storage.save(f"test_folder/{file_name}", ContentFile(file_content))

    # Проверяем, что файл сохранен
    if path:
        return JsonResponse({"message": "File uploaded successfully", "file_path": path})
    else:
        return JsonResponse({"message": "File upload failed"}, status=500)
