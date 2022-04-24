from django.db import models


class BaseModel(models.Model):
    """
    Base Model for fields common to most models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    @property
    def delete(self):
        """
        The aim is not to totally remove the object from the db,
        but to mark it as deleted.
        """
        self.is_deleted = True
        self.save()

    class Meta:
        abstract = True
        ordering = ["-id"]
