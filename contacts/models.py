from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    document = models.FileField(
        upload_to='contact_docs/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx', 'txt'])],
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='contacts'
        )


    class Meta:
        unique_together = ('name', 'email')
        
    def __str__(self):
        return f"{self.name} <{self.name}>"