from requests import get as requests_get, Response
from bs4 import BeautifulSoup
from typing import List, Dict
from json import dump as json_dump
from sys import stderr
import logging

logger = logging.getLogger('devto')

class DevTo:
    
    @classmethod
    def top_tags_api(cls, count: int) -> List[Dict]:
        """
        Get the {count} most popular tags from the dev.to API.
        See https://developers.forem.com/api/v0#tag/tags/operation/getTags
        """
        return cls.get_200(f'https://dev.to/api/tags?per_page={count}&page=0').json()
    
    @classmethod
    def top_tags(cls) -> List[Dict]:
        """
        Get the top tags (currently 100) from the page https://dev.to/tags (HTML parsing).
        The extracted information is the tag name, and number of posts ("XXX posts published").
        IMPORTANT: the number of posts may be off (see article_count_for_tag).
        """
        res = cls.get_200(f'https://dev.to/tags')
        soup = BeautifulSoup(res.content, 'html.parser')

        tags = []
        for tag_card in soup.select('div.tag-card'):
            tags.append({
                'name': tag_card.find('h3').text.strip()[1:],
                'num_articles': int(tag_card.select('p')[-1].text.strip().split(" ")[0])
            })

        return tags


    @classmethod
    def top_articles(cls, count: int, *tags) -> List[Dict]:
        """
        Get the most popular articles of all time, with an optional tag filter.
        Results include user, metadata (id, title, reading time, date, ...) and 
        counters (public_reactions_count, comments_count).
        """
        tag_query = f"&tag_names[]={', '.join(tags)}" if tags else ''
        return cls._paginated(
            count, 
            'https://dev.to/search/feed_content?' \
                f'class_name=Article&per_page={count}&sort_by=public_reactions_count&sort_direction=desc{tag_query}',
            lambda res: res.json()['result']
        )

    @classmethod
    def article_count_for_tag(cls, tag: str) -> int:
        """
        Get the number of articles for a specific tag, according to the https://dev.to/t/{tag} page (HTML parsing).
        Note that this count is often different (lower, more accurate ?) than the one 
        displayed on the https://dev.to/tags page.
        """
        res = cls.get_200(f'https://dev.to/t/{tag}/top/infinity')
        soup = BeautifulSoup(res.content, 'html.parser')
        published_posts_text = soup.select("div.sidebar-data > div")[0].text
        return int(published_posts_text.strip().split(" ")[0])

    
    @classmethod
    def _paginated(cls, count: int, url: str, extracter) -> List[Dict]:
        results = []
        page = 0
        while len(results) < count:
            current = extracter(cls.get_200(f'{url}&page={page}'))
            if len(current) == 0:
                logger.info('No more pages available for {url} (page={page})')
                break
            results += current
            page += 1
        return results


    @staticmethod
    def get_200(url: str) -> Response:
        logger.debug(f'Getting url: {url}')
        res = requests_get(url)
        if res.status_code != 200:
            raise Exception(f'Unable to fetch page {url}: {res.status_code}: {res.text}')
        return res

if __name__ ==  "__main__":

    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', stream=stderr)
    logging.getLogger('devto').level = logging.DEBUG

    def top_articles():
        articles = DevTo.top_articles(10_000)
        with open('top_articles.json', 'w') as f:
            json_dump(articles, f, indent=2)
    
    def top_articles_by_tag():
        articles_by_tags = []
        for t in DevTo.top_tags(): # to use the API -> DevTo.top_tags(100)
            tag = t['name']
            try:
                articles_by_tags.append({
                    'tag': t,
                    'top_articles': DevTo.top_articles(100, tag),
                    'total': DevTo.article_count_for_tag(tag) 
                })
            except Exception as e:
                print(f'problem fetching {tag}: {e}')

        with open('top_articles_by_tag.json', 'w') as f:
            json_dump(articles_by_tags, f, indent=2)
    
    top_articles()
    top_articles_by_tag()