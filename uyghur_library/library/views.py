from os import name
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .forms import BookForm
from .models import Book


def home(request):
    return render(request, 'library/home.html')

def about(request):
    return render(request, 'library/about.html')

def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'library/upload.html', context)


def book_list(request):
    books = Book.objects.all()
    return render(request, 'library/book_list.html', {
        'books': books
    })


def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'library/upload_book.html', {
        'form': form
    })


def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')
    
# class BookListView(ListView):
#     model = Book
#     template_name = 'class_book_list.html'
#     context_object_name = 'books'


# class UploadBookView(CreateView):
#     model = Book
#     form_class = BookForm
#     success_url = reverse_lazy('class_book_list')
#     template_name = 'upload_book.html'
