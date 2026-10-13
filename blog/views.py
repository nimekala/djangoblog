from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import PostForm, RegisterForm
from .models import Post, Category


def _published_posts():
    return (Post.objects.filter(status="published")
            .select_related("category", "author")
            .prefetch_related("tags")
            .order_by("-created_at"))


def home(request):
    paginator = Paginator(_published_posts(), 6)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "blog/home.html", {
        "page_obj": page_obj,
        "categories": Category.objects.all().order_by("name"),
    })


def category_list(request):
    categories = Category.objects.all().order_by("name")
    return render(request, "blog/category_list.html", {"categories": categories})


def category_posts(request, pk):
    category = get_object_or_404(Category, pk=pk)
    paginator = Paginator(_published_posts().filter(category=category), 6)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "blog/home.html", {
        "page_obj": page_obj,
        "current_category": category,
        "categories": Category.objects.all().order_by("name"),
    })


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user   # author එක user තෝරන්නේ නෑ, අපි දානවා
            post.save()
            form.save_m2m()              # commit=False වෙලාවට tags වෙනම save කරන්න ඕන
            if post.status == "published":
                messages.success(request, "Post published successfully!")
                return redirect("post_detail", slug=post.slug)
            messages.success(request, "Draft saved.")
            return redirect("my_posts")
    else:
        form = PostForm(initial={"status": "published"})
    return render(request, "blog/post_form.html", {"form": form})


@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        raise PermissionDenied   # 403 Forbidden
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, "Post updated.")
            if post.status == "published":
                return redirect("post_detail", slug=post.slug)
            return redirect("my_posts")
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_form.html", {"form": form, "editing": True})


@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        raise PermissionDenied
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect("home")
    return render(request, "blog/post_confirm_delete.html", {"post": post})


@login_required
def my_posts(request):
    posts = (Post.objects.filter(author=request.user)
             .select_related("category")
             .order_by("-created_at"))
    page_obj = Paginator(posts, 6).get_page(request.GET.get("page"))
    return render(request, "blog/my_posts.html", {"page_obj": page_obj})


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "blog/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


def about(request):
    return render(request, "blog/about.html")


def contact(request):
    return render(request, "blog/contact.html")


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    # draft එකක් බලන්න පුළුවන් author ට විතරයි
    if post.status != "published" and post.author != request.user:
        raise Http404
    return render(request, "blog/post_detail.html", {"post": post})


def custom_403(request, exception=None):
    return render(request, "blog/403.html", status=403)