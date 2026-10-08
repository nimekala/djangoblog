from django.contrib.auth import login
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import PostForm, RegisterForm
from .models import Post, Category


def _published_posts():
    return (Post.objects.filter(status="published")
            .select_related("category")
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


def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            if post.status == "published":
                return redirect("post_detail", slug=post.slug)
            return redirect("home")
    else:
        form = PostForm(initial={"status": "published"})
    return render(request, "blog/post_form.html", {"form": form})


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "blog/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)  # මුලින් user එක save වෙනවා
        login(self.request, self.object)     # ඊට පස්සේ ඒ user ව ඉබේම login කරනවා
        return response


def about(request):
    return render(request, "blog/about.html")


def contact(request):
    return render(request, "blog/contact.html")


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status="published")
    return render(request, "blog/post_detail.html", {"post": post})