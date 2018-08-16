from datetime import datetime
from mongoengine import DoesNotExist
from mongoengine.queryset.visitor import Q
from newspaper import Article
from requests import head
from tldextract import extract
from urllib.parse import urlparse

from models.Topic import Topic
from models.News import News


def short_url(url):
    return head(url, allow_redirects=True).url


def get_link_info(link):
    parsed_uri = urlparse(link)
    source = '{uri.netloc}'.format(uri=parsed_uri)
    domain = extract(link).domain

    article = Article(link)
    article.build()
    try:
        full_text = article.text
    except:
        full_text = None
        pass

    image = article.top_image
    keywords = article.keywords
    summary = article.summary
    title = article.title
    published_at = article.publish_date

    try:
        language = article.meta_lang
    except:
        language = None
        pass

    try:
        author = article.authors
    except:
        author = None
        pass

    if image != "" and full_text != "" and title != "":
        dic = {'url': link, 'image': image, 'title': title, 'domain': domain, 'full_text': full_text,
               'summary': summary, 'keywords': keywords, 'source': source,
               'published_at': published_at, 'language': language, 'authors': author}
        print('done')
        return dic


def update_news(topic, news, mention, short_link):
    news.update(add_to_set__mentions=mention)
    news.update(add_to_set__short_links=short_link)
    news.reload()

    topic.last_news_at = datetime.now
    topic.save()


def save_news(topic, news_data):
    news = News()
    news.topic_id = topic.id
    news.title = news_data['title']
    news.full_text = news_data['full_text']
    news.summary = news_data['summary']
    news.published_at = news_data['published_at']
    news.image = news_data['image']
    news.url = news_data['url']
    news.source = news_data['source']
    news.domain = news_data['domain']
    news.authors = news_data['authors']
    news.language = news_data['language']
    news.mentions = news_data['mentions']
    news.short_links = news_data['short_links']
    news.save()

    topic.last_news_at = datetime.now
    topic.save()


def parse_links(topic_id, data):
    try:
        topic = Topic.objects.get(id=topic_id)
    except DoesNotExist:
        return
    urls = data['urls']
    del data['urls']
    for link in urls:
        short_link = link
        link = short_url(link)

        try:
            news = News.objects.get(Q(topic_id=topic_id) & (Q(url=link) | Q(short_links=short_link)))
            update_news(topic, news, data, short_link)
        except DoesNotExist:
            dic = get_link_info(link)
            if dic is not None:
                try:
                    news = News.objects.get(Q(topic_id=topic_id) & (Q(domain=dic['domain']) | Q(title=dic['title'])))
                    update_news(topic, news, data, short_link)
                except DoesNotExist:
                    dic['mentions'] = [data]
                    dic['short_links'] = [short_link]
                    save_news(topic, dic)