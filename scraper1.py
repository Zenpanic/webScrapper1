import requests
from bs4 import BeautifulSoup
import pprint
import sys

pages = 1

if len(sys.argv) == 2:
    if 0 < int(sys.argv[1]) < 100:
        pages = int(sys.argv[1])


def getting_pages(pages):

    page_list = []
    full_list = {}

    for page in range(pages):

        res = requests.get(f'https://news.ycombinator.com/news?p={page+1}')
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.storylink')
        subtext = soup.select('.subtext')
        page_list.append({'links': links, 'subtext': subtext})

    print(type(page_list[0]))

    for page in page_list:

        if not 'links' in full_list:
            full_list['links'] = page['links']
        else:
            full_list['links'] = full_list.get(
                'links') + page['links']

        if not 'subtext' in full_list:
            full_list['subtext'] = page['subtext']
        else:
            full_list['subtext'] = full_list.get(
                'subtext') + page['subtext']

    return full_list


def sort_stories_by_votes(hnlist):

    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):

    hn = []

    for i, item in enumerate(links):
        title = links[i].getText()
        href = links[i].get('href', None)
        vote = subtext[i].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points >= 100:
                hn.append({'title': title, 'link': href, 'votes': points})

    return sort_stories_by_votes(hn)


full_list = getting_pages(pages)

pprint.pprint(create_custom_hn(full_list['links'], full_list['subtext']))
