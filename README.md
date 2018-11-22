# Watchtower-News

Watchtower-News is a topic-based news-feed generator. 

- Collect fresh and popular **news**, **articles** and **blog posts** around **topics that you define**. 
- Publish this collected content through an **API**.
- **Self-hosted** and **open source**.

## Why We Have Started This Project?

In a project we have needed to curate news, articles, blog posts for a (maker) community. We evaluated different solutions:
- We didn’t have enough budget for **commercial solutions**: [newsapi.org](https://www.newsapi.org), [webhose.io](https://www.webhose.io), [datastreamer.io](https://www.datastreamer.io), [twingly](https://www.twingly.com), [Aylien News API](https://www.aylien.com/news-api).

- [News-please](https://github.com/fhamborg/news-please) and [twitter-news](https://github.com/mishakob/twitter-news) require to specify URL of news websites and twitter handles respectively. We didn’t want to create and maintain such lists. Since the content is technical and the sources are spread around many websites / twitter accounts.

## How It Works?

1. Collect tweets containing keywords that you define via [Twitter Streaming API](https://developer.twitter.com/en/docs/tweets/filter-realtime/overview),
2. For a tweet contaning a link, follow the link to the end,
3. Process the content: get the title, publish date, predict the language, summarize the content, select a representative image,
4. Store raw and processed data on database (MongoDB),
5. Publish data through an API.

## Getting Started

### Prerequisites

Docker and Docker Compose

### Installing

`$ cp .env-example .env`

Fill the .env file.

`$ bash run.sh`

### License
This project is licensed under the MIT License.
