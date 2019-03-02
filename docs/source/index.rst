Welcome to Pytedjmi's documentation!
====================================

Contents:

.. toctree::
   :maxdepth: 2


Pytedjmi is a tool for testing Django migrations with Pytest.

It handles all of the migration set up and tear down for you, but you
have to define the before-state and the after-state that you want for
your test.

Here's an example:

.. code-block:: python

   import pytest
   import pytedjmi


   # We are changing our data model from one-to-many Authors-to-Books to
   # many-to-many Authors-to-Books, because we want to support collaborations.
   @pytest.mark.django_db
   @pytedjmi.cleanup
   def test_books_and_authors_data_migration():
       # First, we roll back:
       old_apps = pytedjmi.migrate("app_name", "0011_add_book_model")
       Book = old_apps.get_model('library', 'Book')
       Author = old_apps.get_model('library', 'Author')
       a_book = Book.objects.create(title='Moby-Dick')
       Author.objects.create(book=a_book, name='Herman Melville')

       # Then, we roll forward and get the new models:
       new_apps = pytedjmi.migrate(
           "app_name",
           "0012_book_author_m2m_data_migration",
       )
       Book = new_apps.get_model('library', 'Book')
       Author = new_apps.get_model('library', 'Author')
       author = Author.objects.first()
       book = Book.objects.first()

       assert list(book.author_set.all()) == [author]
       assert list(author.book_set.all()) == [book]


Depending on your database backend and the migrations you run, you may
need to include ``pytest-django``'s ``transactional_db`` fixture. If you
see errors telling you about pending trigger events, this is probably
the fix you need.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
