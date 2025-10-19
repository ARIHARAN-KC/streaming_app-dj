# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Video

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'thumbnail', 'video_file']  # Ensure 'video_file' is in the model

class ProfileForm(forms.ModelForm):
    # You can extend this form to include fields like bio, email, etc.

    class Meta:
        model = User  # If you're using the default User model
        fields = ['email']  # Here, you can define fields you want to be editable

    # Custom fields
    profile_picture = forms.ImageField(required=False)  # Optional for uploading a new profile picture
    bio = forms.CharField(widget=forms.Textarea, required=False, max_length=500, label="Short Bio")

    # You can also add more fields here if you are extending the User model with a UserProfile

    # Clean method (optional)
    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        # You can add validation for picture size, type, etc.
        return picture