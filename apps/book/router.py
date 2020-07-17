from rest_framework.routers import DefaultRouter

from .views import PublishViewSet
from .views import AuthorViewSet
from .views import BookViewSet
# from .views import PublishViewSets
# from .views import AuthorViewSets
# from .views import BookViewSets

books_router = DefaultRouter()

# books_router.register(r'pub',PublishViewSets)
# books_router.register(r'aut',AuthorViewSets)
# books_router.register(r'boo',BookViewSets)

books_router.register(r'books/publish', PublishViewSet)
books_router.register(r'books/author', AuthorViewSet)
books_router.register(r'books/book', BookViewSet)


