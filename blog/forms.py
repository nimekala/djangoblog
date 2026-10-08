from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "category", "tags", "content", "cover_image", "status"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "tags": forms.CheckboxSelectMultiple(),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 8}),
            "cover_image": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }

    def clean_cover_image(self):
        image = self.cleaned_data.get("cover_image")
        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file too large (max 5MB).")
            valid_extensions = [".jpg", ".jpeg", ".png", ".webp"]
            if not any(image.name.lower().endswith(ext) for ext in valid_extensions):
                raise forms.ValidationError("Unsupported file type. Use JPG, PNG, or WEBP.")
        return image