import requests
from bs4 import BeautifulSoup
from datetime import datetime
import dateparser

def get_html_content(url):
    response = requests.get(url)
    return response.text

def extract_data_from_tags(tags):
    for tag in tags:
        title_tag = tag.find_all(['div'], class_='o-category-link-wrap')
        h3_tags = tag.find_all(['h3'], id='title-of-a-story')
        time_tag = tag.find_all(['time'], class_='c-timestamp')

        if h3_tags and time_tag:
            title_text = h3_tags[0].text.strip().replace('\xa0', '')
            time_text = time_tag[0].text.strip().replace('\xa0', '')
            main_title = title_tag[0].text
            main_time_date = dateparser.parse(time_text, languages=['en'])

            yield {
                'title': title_text,
                'time': time_text,
                'new_time': main_time_date,
                'm_title':  main_title
            }
        else:
            yield {'error': "No h3 tag with id 'title-of-a-story' found in the current tag."}


'''

def main():
    url = 'https://www.billboard.com/c/music/music-news/'
    pop_url = 'https://www.billboard.com/c/music/pop/'
    hip_url = 'https://www.billboard.com/c/music/rb-hip-hop/'
    latin_url = 'https://www.billboard.com/c/music/latin/'
    rock_url = 'https://www.billboard.com/c/music/rock/'
    awards_url = 'https://www.billboard.com/c/music/rock/'

    # Get HTML content
    html_content = get_html_content(url)

    # Initialize BeautifulSoup with the HTML content
    site = BeautifulSoup(html_content, 'html.parser')

    # Find tags with specified criteria
    tags = site.find_all(['div'], class_="a-story-grid")

    # Extract and print data
    for data in extract_data_from_tags(tags):
        print(data['img'])

if __name__ == "__main__":
    main()
'''
