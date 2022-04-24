from core.models import BaseModel
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(BaseModel, AbstractUser):
    """
    Custom user model to hold the customer information.

    We will use the default active settings to register new users
    With no user activation.
    """

    email = models.EmailField(
        _("Email address"), help_text=_("Enter email address."), unique=True, blank=True
    )
    password = models.CharField(
        _("Password"), help_text=_("Enter a password."), max_length=100
    )

    REQUIRED_FIELDS = ["email", "password"]

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        if self.email:
            return self.email
        return self.username

    def __repr__(self) -> str:
        return super().__repr__()
