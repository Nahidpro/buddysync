from django.db import models
from django.conf import settings  
from django.contrib.auth import get_user_model
import uuid


User = get_user_model() 

class Follow(models.Model):
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('followed_user', 'following_user')  
    def __str__(self):
        return f"{self.following_user} follows {self.followed_user}"

    


class Friend(models.Model):
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('from_user', 'to_user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username} ({self.status})"


