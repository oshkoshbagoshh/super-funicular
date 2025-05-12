from django.db import models

# Create your models here.
class Genre(models.Model):
    """Model representing a music genre."""
    name = models.CharField(max_length=200, help_text='Enter a music genre (e.g. Rock, Jazz, Hip Hop)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Artist(models.Model):
    """Model representing a music artist."""
    name = models.CharField(max_length=200, help_text='Enter the artist name')
    bio = models.TextField(max_length=1000, help_text='Enter a brief bio of the artist', blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Album(models.Model):
    """Model representing a music album."""
    title = models.CharField(max_length=200, help_text='Enter the album title')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this album')
    release_date = models.DateField(null=True, blank=True)
    cover_image = models.CharField(max_length=500, help_text='URL to album cover image', default='https://via.placeholder.com/300')

    def __str__(self):
        """String for representing the Model object."""
        return self.title

class Track(models.Model):
    """Model representing a music track."""
    title = models.CharField(max_length=200, help_text='Enter the track title')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='tracks')
    audio_file = models.CharField(max_length=500, help_text='URL to audio file', default='https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3')
    duration = models.CharField(max_length=10, help_text='Duration of the track (e.g. 3:45)', blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.title
