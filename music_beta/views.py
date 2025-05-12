from django.shortcuts import render
from .models import Genre, Artist, Album, Track

# Create your views here.
def home(request):
    """
    View function for the home page of the site.
    """
    return render(request, 'music_beta/home.html')

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
