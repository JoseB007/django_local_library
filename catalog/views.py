from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect


import datetime


from .forms import RenewBookForm

# Create your views here.


def index(request):
    # Genera contadores de algunos de los objetos principales
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Libros disponibles (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='d').count()
    # El 'all()' esta implícito por defecto.
    num_authors = Author.objects.count()
    num_genre = Genre.objects.count()
    el_books = Book.objects.filter(title__icontains='el').count()

    # Sesiones
    # del request.session['num_visitas']
    num_visitas = request.session.get('num_visitas', 0)
    request.session['num_visitas'] = num_visitas + 1


    #  Dicionario de variables
    context={'num_books': num_books, 
            'num_instances': num_instances,
            'num_instances_available': num_instances_available, 
            'num_authors': num_authors, 
            'num_genre': num_genre, 
            'el_books': el_books,
            'num_visitas': num_visitas}
 
    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(request, 'index.html', context=context)


class BookListView(ListView):
    model = Book
    template_name = 'catalog/book_list.html'
    context_object_name = 'book_list'
    paginate_by = 2


class BookDetailView(DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'
    context_object_name = 'book'


class AuthorListView(ListView):
    model = Author
    template_name = 'catalog/author_list.html'
    context_object_name = 'author_list'


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        # Obtenemos el contexto generado por la vista padre
        context = super().get_context_data(**kwargs)
        # Obtenemos el autor actual
        author = self.get_object()
        # Obtenemos todos los libros asociados a este autor
        books = Book.objects.filter(author_id=author)
        # Añadimos los libros al contexto
        context['books'] = books
        print(books)
        return context


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='p').order_by('due_back')
    

class LibrosPrestadosPorBiblioteca(PermissionRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalog/librosPrestadosBiblioteca.html'
    permission_required =  'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='p')
    


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})


from django.urls import reverse_lazy

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial={'date_of_death':datetime.date.today(),}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')