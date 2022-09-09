import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

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


def create_question(question_text, days):
  """
  Create a question with the given "question_text", and published the given
  number of days offset to now (negative for question published in the past,
  positive for question that have yet to be published)
  """
  time = timezone.now() + datetime.timedelta(days=days)
  return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):

  def test_no_questions(self):
    """if no question exists, an appropiate message is displayed"""
    response = self.client.get(reverse('polls:index'))
    self.assertEqual(response.status_code, 200)
    self.assertQuerysetEqual(response.context['latest_question_list'], [])
    self.assertContains(response, 'No polls are available')

  def test_future_question(self):
    """Questions with a pub_date in the future aren't displayed on the index page"""
    create_question('Future question', 30)
    response = self.client.get(reverse('polls:index'))
    self.assertEqual(response.status_code, 200)
    self.assertQuerysetEqual(response.context['latest_question_list'], [])
    self.assertContains(response, 'No polls are available')

  def test_past_question(self):
    """Questions with a pub_date in the past are displayed on the index page"""
    question = create_question('Past question', -10)
    response = self.client.get(reverse('polls:index'))
    self.assertEqual(response.status_code, 200)
    self.assertQuerysetEqual(response.context['latest_question_list'], [question])

class QuestionDetailViewTests(TestCase):
  def test_future_questions(self):
    """The detail view of a question with a pub_date in the future returns a 404 error"""
    future_question = create_question('Future question', 30)
    response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
    self.assertEqual(response.status_code, 404)

  def test_past_questions(self):
    """The detail view of a question with a pub_date in the future returns the question"""
    past_question = create_question('Past question', -30)
    response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, past_question.question_text)
