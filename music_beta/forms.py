from django import forms
from .models import Genre

class ServiceRequestForm(forms.Form):
    """Form for service requests."""
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}))
    company = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Company'}))
    service_type = forms.ChoiceField(choices=[
        ('', 'Select Service Type'),
        ('media_solutions', 'Media Solutions'),
        ('music_services', 'Music Services')
    ], required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 4}), required=False)

class UserSignupForm(forms.Form):
    """Form for user signup."""
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class AdCampaignForm(forms.Form):
    """Form for ad campaign upload."""
    title = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Campaign Title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Campaign Description', 'rows': 3}))
    video = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'video/*'}), required=False)
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    mood = forms.ChoiceField(choices=[
        ('', 'Select Mood'),
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('energetic', 'Energetic'),
        ('calm', 'Calm'),
        ('inspirational', 'Inspirational'),
        ('dramatic', 'Dramatic')
    ], widget=forms.Select(attrs={'class': 'form-control'}))
    target_audience = forms.ChoiceField(choices=[
        ('', 'Select Target Audience'),
        ('general', 'General'),
        ('youth', 'Youth'),
        ('adults', 'Adults'),
        ('seniors', 'Seniors'),
        ('professionals', 'Professionals')
    ], widget=forms.Select(attrs={'class': 'form-control'}))
