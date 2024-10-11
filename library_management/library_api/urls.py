from django.urls import path, include

from library_api.views.books import BooksView, BookDetailView
from library_api.views.members import MembersView, MemberDetailView
from library_api.views.transactions import TransactionsView, TransactionDetailView, TransactionReturnView


urlpatterns = [
   path("books/", BooksView.as_view()),
   path("book/<int:pk>/", BookDetailView.as_view()),
   path("members/", MembersView.as_view()),
   path("member/<int:pk>/", MemberDetailView.as_view()),
   path("transactions/", TransactionsView.as_view()),
   path("transaction/<int:pk>/", TransactionDetailView.as_view()),
   path("book/return", TransactionReturnView.as_view())
]
