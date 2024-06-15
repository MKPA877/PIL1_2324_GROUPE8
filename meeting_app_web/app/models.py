from django.contrib.auth.models import AbstractUser
from django.db import models


"""def upload_profile_picture(instance, filename):
    path = f'profile_pictures/{instance.username}'
    extension = filename.split('.')[-1]
    if extension:
        path = path + '.' + extension
    return path"""


class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    #username = models.CharField(max_length=30)
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=gender_choices)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    profile_picture = models.ImageField(
        upload_to="images/profile_pictures/",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Connection(models.Model):
	sender = models.ForeignKey(
		User,
		related_name='sent_connections',
		on_delete=models.CASCADE
	)
	receiver = models.ForeignKey(
		User,
		related_name='received_connections',
		on_delete=models.CASCADE
	)
	accepted = models.BooleanField(default=False)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.sender.username + ' -> ' + self.receiver.username



class Message(models.Model):
    connection = models.ForeignKey(
        Connection,
        related_name='messages',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        related_name='my_messages',
        on_delete=models.CASCADE
    )
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='messages/images/', null=True, blank=True)
    video = models.FileField(upload_to='messages/videos/', null=True, blank=True)
    document = models.FileField(upload_to='messages/documents/', null=True, blank=True)
    audio = models.FileField(upload_to='messages/audio/', null=True, blank=True)
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ': ' + (self.text if self.text else 'Media message')



class CentresDInteret(models.Model):
    user = models.OneToOneField(
        User,
        related_name='centres_d_interet',
        on_delete=models.CASCADE
    )
    sport = models.BooleanField(default=False)
    musique = models.BooleanField(default=False)
    lecture = models.BooleanField(default=False)
    voyage = models.BooleanField(default=False)
    cinema = models.BooleanField(default=False)
    technologie = models.BooleanField(default=False)

    def __str__(self):
        return f'Centres d\'intérêt de {self.user.username}'

class CustomUser(AbstractUser):
    profile.picture = models.ImageField(upload_to='profile_pictures\', blank=True, null=True)

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_picture/', blank=True, null=True)
    bio = models.TextField(max_lenght=500, blank=True)
    