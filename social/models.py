from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

import hashlib


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name="added_by")
    added_at = models.DateTimeField(auto_now_add=True)
    unique_hash = models.CharField(max_length=64, unique=True, editable=False)

    class Meta:
        unique_together = ("user", "contact")

    def save(self, *args, **kwargs):
        # Ensure user and contact are in a consistent order
        if self.user.id < self.contact.id:
            user_id = self.user.id
            contact_id = self.contact.id
        else:
            user_id = self.contact.id
            contact_id = self.user.id

        # Generate a consistent unique hash
        unique_string = f"{user_id}{contact_id}"
        self.unique_hash = hashlib.sha256(unique_string.encode()).hexdigest()

        # Check if a reverse contact already exists
        existing_contact = Contact.objects.filter(unique_hash=self.unique_hash).first()

        if existing_contact:
            self.id = existing_contact.id
        else:
            super(Contact, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} -> {self.contact.email}"
