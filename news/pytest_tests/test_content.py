from django.conf import settings
from django.urls import reverse

from news.forms import CommentForm


def test_home_page(client, news_10, settings):
    urls = reverse('news:home')
    response = client.get(urls)
    object_list = response.context['object_list']
    assert len(object_list) == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, news_10):
    urls = reverse('news:home')
    response = client.get(urls)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    assert all_dates == sorted(all_dates, reverse=True)


def test_detail_page_contains_form(author_client, news, form_data):
    url = reverse('news:detail', args=(news.id,))
    response = author_client.get(url, data=form_data)
    assert 'form' in response.context
    form = response.context['form']
    assert isinstance(form, CommentForm)


def test_detail_page_contains_form_for_user(client, news):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert 'form' not in response.context


def test_comments_order(client, news, comments):
    url = reverse('news:detail', args=(news.id,))
    response = client.get(url)
    assert 'news' in response.context
    news_object = response.context['news']
    all_comments = news_object.comment_set.all()
    all_date_created = [comment.created for comment in all_comments]
    assert all_date_created == sorted(all_date_created)
