import datetime

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Question(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text
    
    def days_published(self):
        now = timezone.now()
        day = now - self.pub_date
        return day

    def get_total_vote(self):
        choices = self.choice_set.all()
        global total_votes
        total_votes=0
        for choice in choices:
            total_votes = total_votes + choice.votes
        return total_votes


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
        
    def get_percentage(self):
        try:
            percentage = (self.votes/total_votes)*100
        except(ZeroDivisionError):
            percentage = 0
        return percentage
