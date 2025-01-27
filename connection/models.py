from django.db import models
from django.conf import settings  
from django.contrib.auth import get_user_model

User = get_user_model() 

class Follow(models.Model):
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('followed_user', 'following_user')  
    def __str__(self):
        return f"{self.following_user} follows {self.followed_user}"

    



class Friendship(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendship_user2')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')  

    def __str__(self):
        return f"{self.user1} and {self.user2} are friends"

