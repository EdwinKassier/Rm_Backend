
# todo/models.py
      
from django.db import models
# Create your models here.

#Email and email related libraries
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.conf import settings
from django.core.mail import send_mail
from django_model_changes import ChangesMixin
from django.dispatch import receiver




#Creating the schema for the model
class Todo(ChangesMixin,models.Model):
  title = models.CharField(max_length=120)
  email = models.TextField()
  description = models.TextField()
  assignee =  models.TextField()
  completed = models.BooleanField(default=False)
      
  def __str__(self):
    return self.title

'''Note, the following code while a good showcase of how to send emails at the smaller scale, at larger scale this approach will result in issues like emails being sent to the spam folder as well as not coping well when using custom HTML, which would also cause emails to be flagged as spam.
The ideal solution would be to use a service like mandril/mailchimp to ensure delivery as well as handle potential future requirements
'''

#This function listens for inserts to the model
#As I haven't provided a real email, it will resolve to a "535, b'5.7.8 Username and Password not accepted." error"
#This could be made functional by providing the right credentials
@receiver(pre_save, sender=Todo)
def send_email_if_flag_enabled(sender, instance, **kwargs):
  try:
    subject = 'Future Forex request for documents'
    message = 'Hello %s,\n\n one of our client relationship managers (%s) requires the following documents from you: \n\n%s\n\nYou can upload these documents using our document uploads page.\n\nBest regards,\n\nThe Future Forex Team' %(instance.title,instance.assignee,instance.description)
    from_email = settings.EMAIL_HOST_USER
    print(message)
    if(instance.completed == False):
      send_mail(subject, message, from_email, [instance.email], fail_silently=False)
    else:
      print('This user has completed their file uploads')
  except Exception as e:
    print(e)