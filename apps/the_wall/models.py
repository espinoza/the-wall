from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from ..login.views import User


def make_validators(model_string):
    cant_send = "You can't send such a short "
    limit_reached = "Limit length reached for "
    validators = [MinLengthValidator(limit_value=2, message=cant_send+model_string),
                  MaxLengthValidator(limit_value=10000, message=limit_reached+model_string)]
    return validators


class Message(models.Model):
    content = models.TextField(max_length=10000, validators=make_validators("message"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")


class Comment(models.Model):
    content = models.TextField(max_length=10000, validators=make_validators("comment"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")

