from django.db import models
from django.conf import settings
from django import forms
from django.utils import timezone
# Create your models here.
def x_ago_helper(diff):
    if diff.days > 0:
        return f'{diff.days} days ago'
    if diff.seconds < 60:
        return f'{diff.seconds} seconds ago'
    if diff.seconds <3600:
        return f'{diff.seconds //60} minutes ago'
    return f'{diff.seconds // 3600} hours ago'
class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length =200)
    body = models.TextField(blank =True ,null=True)
    created =models.DateTimeField(editable =False,null=True ,blank=True)
    modified =models.DateTimeField()
    answers_count = models.IntegerField(default=0)
    points =models.IntegerField(default=0)
    hidden =models.BooleanField(default =False)

    @property
    def num_answers(self):
        answers=Answer.objects.filter(question_id =self.id)
        return len(answers)
        #print(answers)
    def x_ago(self):
        diff =timezone.now() - self.created
        return x_ago_helper(diff)
    def save(self,*args,**kwargs):
        if not self.id:
            self.created =timezone.now()
        self.modified =timezone.now()
        return super(Question,self).save(*args,**kwargs)
    def __str__(self):
        return '{}'.format(self.title)


class QuestionForm(forms.Form):
    title =forms.CharField(max_length=200,label="Question",
    widget =forms.TextInput(attrs={'type': 'Textarea','placeholder':'Enter ur question here'}))
    body =forms.CharField(max_length=5000,required =False,label="Details",
    widget=forms.Textarea(attrs={'placeholder': 'Enter details'}))

class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    text =models.TextField()
    created =models.DateTimeField(editable =False,null=True ,blank=True)
    modified =models.DateTimeField()
    points =models.IntegerField(default =0)

    @property
    def x_ago(self):
        diff =timezone.now() - self.created
        return x_ago_helper(diff)

    def save(self,*args,**kwargs):
        if not self.id:
            self.created =timezone.now()
        self.modified =timezone.now()
        return super(Answer,self).save(*args,**kwargs)

    def __str__(self):
        return '{}'.format(self.text)

class AnswerForm(forms.Form):
    text =forms.CharField(max_length=5000,label ='',widget=forms.Textarea(attrs={'placeholder':'type your answer'}))
