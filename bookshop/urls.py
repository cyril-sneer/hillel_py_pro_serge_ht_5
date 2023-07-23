from django.urls import path
from . import views

app_name = "bookshop"

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('stores/', views.StoreListView.as_view(), name='stores'),
    path('store/<int:pk>', views.StoreDetailView.as_view(), name='store-detail'),
    path('publishers/', views.PublisherListView.as_view(), name='publishers'),
    path('publisher/<int:pk>', views.PublisherDetailView.as_view(), name='publisher-detail'),
]

urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
]