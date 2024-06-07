from django.db import models
from django.urls import reverse
# from django.utils.text import slugify
import uuid  # Requerida para las instancias de libros únicos
from django.contrib.auth.models import User
from datetime import date

# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True,
                            help_text="Ingrese el nombre del género (p. ej. Ciencia Ficción, Poesía Francesa etc.)")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    
    # slug = models.SlugField(unique=True)

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # ForeignKey, ya que un libro tiene un solo autor, pero el mismo autor puede haber escrito muchos libros.
    # 'Author' es un string, en vez de un objeto, porque la clase Author aún no ha sido declarada.

    summary = models.TextField(
        max_length=1000, help_text="Ingrese una breve descripción del libro")

    isbn = models.CharField(
        'ISBN', max_length=13, help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text="Seleccione un genero para este libro")
    # ManyToManyField, porque un género puede contener muchos libros y un libro puede cubrir varios géneros.

    def __str__(self):
        return self.title

    # def save(self):
    #     self.slug = slugify(self.title)
    #     super().save()

    def get_absolute_url(self):
        return reverse('book-detail', args=[self.id])

    # def display_genre(self):
    #     genre_names = []  # Crear una lista vacía para almacenar los nombres de los géneros
    #     for genre in self.genre.all():  # Iterar sobre cada género en la lista de géneros
    #         # Agregar el nombre del género a la lista
    #         genre_names.append(genre.name)
    #     # Unir los nombres de los géneros en una sola cadena separada por comas
    #     return ', '.join(genre_names)
    
    def display_genre(self):
        return ', '.join([genre.name for genre in self.genre.all()])


class BookInstance(models.Model):
    #  Modelo que representa una copia específica de un libro (que puede ser prestado por la biblioteca).
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="ID único para este libro particular en toda la biblioteca")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('n', 'No disponible'),
        ('p', 'En prestamo'),
        ('d', 'Disponible'),
        ('r', 'Reservado'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                              blank=True, default='d', help_text='Disponibilidad del libro')
    
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'
    
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.last_name} {self.first_name}'
    
    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
