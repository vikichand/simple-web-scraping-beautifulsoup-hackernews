# pip install beautifulsoup4
# pip install requests

import requests
from bs4 import BeautifulSoup
import pprint

def get_res(pages, links_selector, subtext_selector):
    links = []
    subtext = []

    for page in range(0, pages):
        res = requests.get(f'https://news.ycombinator.com/news?p={page}')
        soup = BeautifulSoup(res.text, 'html.parser')
        links += soup.select('.storylink')
        subtext += soup.select('.subtext')

    return links, subtext

def sort_stories_by_votes(compiled_list):
    return sorted(compiled_list, key = lambda k:k['votes'], reverse = True)

def compile_data(links, subtext, min_votes):
    compiles_data = []

    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')

        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))

            if points > min_votes - 1:
                compiles_data.append({'title': title, 'link': href, 'votes': points})

    return sort_stories_by_votes(compiles_data)

scrape_pages = 2
min_votes = 100
links_selector = '.storylink'
subtext_selector = '.subtext'

mega_links, mega_subtext = get_res(scrape_pages, links_selector, subtext_selector)

pprint.pprint(compile_data(mega_links, mega_subtext, min_votes))