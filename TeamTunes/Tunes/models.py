from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from datetime import datetime

# Create your models here.
class Profile(models.Model):
	"""
	Model representing a user of the site.
	"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this user")
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	bio = models.TextField()
	events_hosting = models.ManyToManyField('Event', related_name = "user_events_hosting", blank = True, null = True)
	events_attending = models.ManyToManyField('Event', related_name = "user_events_attending", blank = True, null = True)
	events_attended = models.ManyToManyField('Event', related_name = "user_events_attended",  blank = True, null = True)
	anthem = models.ForeignKey('Song', on_delete=models.SET_NULL, null = True, related_name = "user_anthem")
	location = models.ForeignKey('Location', on_delete=models.SET_NULL, null = True, related_name = "user_location")
	followers = models.ManyToManyField('Profile', related_name = "user_followers",  blank = True, null = True)
	following = models.ManyToManyField('Profile', related_name = "user_following",  blank = True, null = True)
	rotation = models.ManyToManyField('Album')
	favorite_songs = models.ManyToManyField('Song')
	favorite_genres = models.ManyToManyField('Genre')
	hobbies = models.CharField(max_length=200)
	email = models.EmailField(blank = True, null = True)
	current_song = models.ForeignKey('Song', blank = True, null = True, on_delete=models.SET_NULL, related_name = "user_current_song", help_text="Currently listened to song")
	profile_picture = models.ImageField(upload_to = 'images/users/', default = 'images/default.png', blank = True, null = True)
	playlists = models.ManyToManyField('Playlist', blank = True, null = True, related_name = "playlist_user")
	latitude = models.DecimalField(max_digits=9, decimal_places=6, blank = True, null = True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, blank = True, null = True)

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
	    if created:
	        Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
	    instance.profile.save()

	def __str__(self):
		"""
		String for representing the Model object (in Admin site etc.)
		"""
		return self.name

	def get_absolute_url(self):
		"""
		Returns the url to access a particular user instance.
		"""
		return reverse('user-detail', args=[str(self.id)])

class Event(models.Model):
	"""
	Model representing an event listing.
	"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this event")
	name = models.CharField(max_length=100)
	location = models.ForeignKey('Location', blank = True, null = True, on_delete=models.SET_NULL, related_name = "event_location")
	start_time = models.DateTimeField('Start Time', default=datetime.now, help_text="(yyyy-mm-dd hh:mm:ss)")
	end_time = models.DateTimeField('End Time', default=datetime.now, help_text="(yyyy-mm-dd hh:mm:ss)")
	description = models.TextField()
	image = models.ImageField(upload_to = 'images/events/', default = 'images/default.png', blank = True, null = True)
	host = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name = "event_host")
	people = models.ManyToManyField('Profile', related_name = "people_attending")
	other_events = models.ManyToManyField('Event', related_name = "other_events_occuring")
	web_link = models.URLField('Web Link', max_length=250, blank = True, null = True, help_text="(http(s)://...)")
	venue = models.CharField(max_length=100, blank = True, null = True)
	latitude = models.DecimalField(max_digits=9, decimal_places=6, blank = True, null = True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, blank = True, null = True)

	def __str__(self):
		"""
		String for representing the Model object (in Admin site etc.)
		"""
		return self.name

	def get_absolute_url(self):
		"""
		Returns the url to access a particular event instance.
		"""
		return reverse('event-detail', args=[str(self.id)])

class Song(models.Model):
	"""
	Model representing a song.
	"""
	name = models.CharField(max_length=100)
	artist = models.ManyToManyField('Artist', related_name="song_artist")
	album = models.ManyToManyField('Album', related_name="song_album")
	embed_code = models.CharField(max_length=250, blank = True, null = True)

	def __str__(self):
		"""
		String for representing the Model object (in Admin site etc.)
		"""
		return self.name


class Album(models.Model):
	"""
	Model representing an album.
	"""
	name = models.CharField(max_length=100)
	artist = models.ManyToManyField('Artist', related_name="album_artist")
	genre = models.ManyToManyField('Genre', related_name="album_genre")
	art = models.ImageField(upload_to = 'images/albums/')#upload_to=)


	def __str__(self):
		"""
		String for representing the Model object (in Admin site etc.)
		"""
		return self.name

class Genre(models.Model):
	"""
	Model representing a genre.
	"""
	name = models.CharField(max_length=100)

	def __str__(self):
		"""
		String for representing the Model object (in Admin site etc.)
		"""
		return self.name

class Artist(models.Model):
	"""
	Model representing an artist.
	"""
	name = models.CharField(max_length=100)

	def __str__(self):
		"""
		String for representing the Model object (in Admin site etc.)
		"""
		return self.name

class Location(models.Model):
	"""
	Model representing a location.
	"""
	name = models.CharField(max_length=100, help_text="City Name")
	state = models.CharField(max_length=100)

	def __str__(self):
		"""
		String for representing the Model object (in Admin site etc.)
		"""
		return self.name

class Playlist(models.Model):
	"""
	Model representing a user playlist.
	"""
	name = models.CharField(max_length=250, blank = True, null = True, help_text="Playlist Name")
	embed_code = models.CharField(max_length=450, blank = True, null = True)

	def __str__(self):
		"""
		String for representing the Model object (in Admin site etc.)
		"""
		return self.name
