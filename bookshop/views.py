# Create your views here.

from django.db.models import Avg, Max, Count, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required

from .models import Store, Book, Author, Publisher


def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_stores = Store.objects.count()

    num_books = Book.objects.all().count()
    max_price = Book.objects.aggregate(Max("price")).get("price__max")
    avg_price = Book.objects.aggregate(Avg("price")).get("price__avg")

    num_authors = Author.objects.count()  # Метод 'all()' применён по умолчанию.
    avg_books_per_author = \
        Author.objects.annotate(book_count=Count('book')).aggregate(Avg("book_count")).get('book_count__avg')

    num_publisher = Publisher.objects.count()
    avg_books_per_publisher = \
        Publisher.objects.annotate(book_count=Count('book')).aggregate(Avg("book_count")).get("book_count__avg")

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
        context={'num_stores': num_stores,
                 'num_books': num_books,
                 'max_price': round(max_price, 2),
                 'avg_price': round(avg_price, 2),
                 'num_authors': num_authors,
                 'avg_books_per_author': round(avg_books_per_author),
                 'num_publisher': num_publisher,
                 'avg_books_per_publisher': round(avg_books_per_publisher, 2),
                 'num_visits': num_visits}
    )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 20


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 20


class AuthorDetailView(generic.DetailView):
    model = Author


class PublisherListView(generic.ListView):
    model = Publisher
    paginate_by = 20


class PublisherDetailView(generic.DetailView):
    model = Publisher

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        publisher = context.get('publisher')

        num_books = publisher.book_set.count()
        context['num_books'] = num_books
        return context


class StoreListView(generic.ListView):
    model = Store
    paginate_by = 10


class StoreDetailView(generic.DetailView):
    model = Store

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        store = context.get('store')

        # Add in a QuerySet
        num_books = store.books.count()
        avg_price = store.books.aggregate(Avg('price')).get("price__avg")
        avg_pages = store.books.aggregate(Avg('pages')).get("pages__avg")
        num_authors = \
            store.books.annotate(author_count=Count('authors')).aggregate(Sum("author_count")).get("author_count__sum")
        most_expansive = store.books.order_by('-price')[:20]

        context["num_books"] = num_books
        context["avg_price"] = round(avg_price, 2)
        context["avg_pages"] = round(avg_pages)
        context["num_authors"] = num_authors
        context["most_expansive"] = most_expansive
        return context


class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = '__all__'


class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('bookshop:books/')
