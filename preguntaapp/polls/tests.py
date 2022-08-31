import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

class QuestionModelTest(TestCase):

  def setUp(self):
    self.question = Question(question_text='test_was_published_recently_with_future_questions')

  def test_was_published_recently_with_future_questions(self):
    """was_published_recently returns False for questions whose pub_date is in the future"""
    time = timezone.now() + datetime.timedelta(days=30)
    self.question.pub_date = time
    self.assertFalse(self.question.was_published_recently())

  def test_was_published_recently_with_present_questions(self):
    """was_published_recently returns True for questions whose pub_date is at the moment"""
    time = timezone.now()
    self.question.pub_date = time
    self.assertTrue(self.question.was_published_recently())

  def test_was_published_recently_with_past_questions(self):
    """was_published_recently returns False for questions whose pub_date is more than 1 week in the past"""
    time = timezone.now() - datetime.timedelta(weeks=1, minutes=1)
    self.question.pub_date = time
    self.assertFalse(self.question.was_published_recently())
