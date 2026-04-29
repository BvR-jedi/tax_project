from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post


def index(request):
    posts = Post.objects.all().order_by('-date_created')
    return render(request, 'blog/index.html', {'posts': posts})


def post_list(request):
    posts = Post.objects.all().order_by('-date_created')
    return render(request, 'blog/partials/post_list.html', {'posts': posts})


def post_create(request):
    if request.method == 'POST':
        author = request.POST.get('author')
        title = request.POST.get('title')
        content = request.POST.get('content')
        if author and title and content:
            Post.objects.create(author=author, title=title, content=content)
        posts = Post.objects.all().order_by('-date_created')
        return render(request, 'blog/partials/post_list.html', {'posts': posts})
    return HttpResponse(status=405)


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/partials/post_edit_form.html', {'post': post})


def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.author = request.POST.get('author', post.author)
        post.title = request.POST.get('title', post.title)
        post.content = request.POST.get('content', post.content)
        post.save()
    return render(request, 'blog/partials/post_item.html', {'post': post})


from django.views.decorators.http import require_POST

@require_POST
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return HttpResponse('')


def post_search(request):
    query = request.GET.get('q', '')
    posts = Post.objects.filter(title__icontains=query) | \
            Post.objects.filter(author__icontains=query) | \
            Post.objects.filter(content__icontains=query)
    posts = posts.order_by('-date_created')
    return render(request, 'blog/partials/post_list.html', {'posts': posts})
