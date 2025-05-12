from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
import json
import os

# Try to import requests, but provide a fallback if it's not available
try:
    import requests
except ImportError:
    # Create a simple mock for the requests module
    class MockResponse:
        def __init__(self, status_code=200):
            self.status_code = status_code
            self.json_data = {"photos": []}

        def json(self):
            return self.json_data

    class MockRequests:
        @staticmethod
        def get(url, headers=None):
            return MockResponse()

    requests = MockRequests()

from .models import Genre, Artist, Album, Track, User, AdCampaign, ServiceRequest
from .forms import UserSignupForm, AdCampaignForm, ServiceRequestForm

# Create your views here.
def home(request):
    """
    View function for the home page of the site.
    """
    signup_form = UserSignupForm()
    ad_campaign_form = AdCampaignForm()

    context = {
        'signup_form': signup_form,
        'ad_campaign_form': ad_campaign_form,
    }

    return render(request, 'music_beta/home.html', context)

@csrf_exempt
def signup(request):
    """
    View function for user signup.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            # Check if user already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': 'Username already exists'})
            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': 'Email already exists'})

            # Create new user
            user = User.objects.create(
                username=username,
                email=email,
                password=password  # In a real app, this would be hashed
            )

            return JsonResponse({'success': True, 'message': 'User created successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def upload_ad_campaign(request):
    """
    View function for ad campaign upload.
    """
    if request.method == 'POST':
        try:
            # Handle form data (including file uploads)
            form = AdCampaignForm(request.POST, request.FILES)

            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                video = form.cleaned_data.get('video')
                genre = form.cleaned_data['genre']
                mood = form.cleaned_data['mood']
                target_audience = form.cleaned_data['target_audience']
                username = request.POST.get('username')

                # Get user
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    return JsonResponse({'success': False, 'message': 'User not found'})

                # Create new ad campaign
                ad_campaign = AdCampaign.objects.create(
                    title=title,
                    description=description,
                    video=video,
                    genre=genre,
                    mood=mood,
                    target_audience=target_audience,
                    user=user
                )

                return JsonResponse({
                    'success': True, 
                    'message': 'Ad campaign created successfully',
                    'campaign_id': ad_campaign.id
                })
            else:
                return JsonResponse({'success': False, 'message': 'Invalid form data', 'errors': form.errors})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def search(request):
    """
    View function for search functionality.
    """
    if request.method == 'GET':
        query = request.GET.get('q', '')

        if not query:
            return JsonResponse({'success': False, 'message': 'No search query provided'})

        # Search for artists, albums, tracks, and ad campaigns
        artists = Artist.objects.filter(name__icontains=query).values('id', 'name', 'image')
        albums = Album.objects.filter(title__icontains=query).values('id', 'title', 'cover_image', 'artist__name')
        tracks = Track.objects.filter(title__icontains=query).values('id', 'title', 'artist__name', 'album__title')
        ad_campaigns = AdCampaign.objects.filter(title__icontains=query).values('id', 'title', 'description', 'video_url', 'mood')

        results = {
            'artists': list(artists),
            'albums': list(albums),
            'tracks': list(tracks),
            'ad_campaigns': list(ad_campaigns),
        }

        return JsonResponse({'success': True, 'results': results})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def get_pexels_images(request):
    """
    View function to fetch images from Pexels API.
    """
    if request.method == 'GET':
        query = request.GET.get('q', 'music')

        # Get Pexels API key from environment variables
        api_key = os.environ.get('PEXELS_API_KEY', '')

        if not api_key:
            # Return SVG placeholder images if no API key is available
            svg_placeholders = [
                f'/static/images/blog-{i+1}.svg' for i in range(3)
            ] * 4  # Repeat to get 12 images
            return JsonResponse({'success': True, 'images': svg_placeholders[:10]})

        try:
            # Make request to Pexels API
            headers = {
                'Authorization': api_key
            }
            response = requests.get(f'https://api.pexels.com/v1/search?query={query}&per_page=10', headers=headers)

            if response.status_code == 200:
                data = response.json()
                images = [photo['src']['medium'] for photo in data['photos']]
                return JsonResponse({'success': True, 'images': images})
            else:
                # Return SVG placeholder images if API request fails
                svg_placeholders = [
                    f'/static/images/blog-{i+1}.svg' for i in range(3)
                ] * 4  # Repeat to get 12 images
                return JsonResponse({'success': True, 'images': svg_placeholders[:10]})
        except Exception as e:
            # Return SVG placeholder images if there's an exception
            svg_placeholders = [
                f'/static/images/blog-{i+1}.svg' for i in range(3)
            ] * 4  # Repeat to get 12 images
            return JsonResponse({'success': True, 'images': svg_placeholders[:10], 'error': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def service_request(request):
    """
    View function for handling service requests.
    """
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST)
        if form.is_valid():
            # Save the service request to the database
            service_request = ServiceRequest.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                company=form.cleaned_data['company'],
                service_type=form.cleaned_data['service_type'],
                message=form.cleaned_data['message']
            )

            # Send email notification
            subject = f"New Service Request: {form.cleaned_data['service_type']}"
            message = f"""
            New service request received:

            Name: {form.cleaned_data['name']}
            Email: {form.cleaned_data['email']}
            Company: {form.cleaned_data['company']}
            Service Type: {form.cleaned_data['service_type']}
            Message: {form.cleaned_data['message']}
            """
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                ['hello@tfnms.co'],
                fail_silently=False,
            )

            # Return success message
            return render(request, 'music_beta/service_request.html', {
                'form': ServiceRequestForm(),
                'success': True,
                'message': 'Your service request has been submitted successfully. We will contact you soon.'
            })
    else:
        form = ServiceRequestForm()

    return render(request, 'music_beta/service_request.html', {'form': form})

def music_platform(request):
    """
    View function for the CTV Music platform demo.
    """
    # Get all genres, artists, albums, and tracks
    genres = Genre.objects.all()
    artists = Artist.objects.all()
    albums = Album.objects.all().prefetch_related('genre', 'tracks')
    tracks = Track.objects.all().select_related('artist', 'album')

    # If no data exists, create placeholder data
    if not genres.exists():
        # Create genres
        rock = Genre.objects.create(name='Rock')
        pop = Genre.objects.create(name='Pop')
        hiphop = Genre.objects.create(name='Hip Hop')
        jazz = Genre.objects.create(name='Jazz')
        electronic = Genre.objects.create(name='Electronic')

        # Create artists
        artist1 = Artist.objects.create(
            name='Sample Artist 1',
            bio='Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        )
        artist2 = Artist.objects.create(
            name='Sample Artist 2',
            bio='Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
        )

        # Create albums
        album1 = Album.objects.create(
            title='Sample Album 1',
            artist=artist1,
            release_date='2023-01-01',
            cover_image='https://via.placeholder.com/300'
        )
        album1.genre.add(rock, pop)

        album2 = Album.objects.create(
            title='Sample Album 2',
            artist=artist2,
            release_date='2023-02-01',
            cover_image='https://via.placeholder.com/300'
        )
        album2.genre.add(hiphop, electronic)

        # Create tracks
        Track.objects.create(
            title='Sample Track 1',
            album=album1,
            artist=artist1,
            audio_file='https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
            duration='3:45'
        )
        Track.objects.create(
            title='Sample Track 2',
            album=album1,
            artist=artist1,
            audio_file='https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3',
            duration='4:12'
        )
        Track.objects.create(
            title='Sample Track 3',
            album=album2,
            artist=artist2,
            audio_file='https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3',
            duration='3:22'
        )
        Track.objects.create(
            title='Sample Track 4',
            album=album2,
            artist=artist2,
            audio_file='https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3',
            duration='5:01'
        )

        # Refresh querysets
        genres = Genre.objects.all()
        artists = Artist.objects.all()
        albums = Album.objects.all().prefetch_related('genre', 'tracks')
        tracks = Track.objects.all().select_related('artist', 'album')

    context = {
        'genres': genres,
        'artists': artists,
        'albums': albums,
        'tracks': tracks,
    }

    return render(request, 'music_beta/music_platform.html', context)
