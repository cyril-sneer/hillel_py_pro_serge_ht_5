from django.contrib import admin

# Register your models here.

from bookshop.models import Author, Publisher, Store, Book


class BooksInline(admin.TabularInline):
    model = Book
    extra = 0


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'age']
    list_filter = ['age']


class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [BooksInline]


class BookAdmin(admin.ModelAdmin):
    list_display = ["name", "pages", "price", "publisher", "pubdate"]
    list_filter = ["pubdate"]


class StoreAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Store, StoreAdmin)



