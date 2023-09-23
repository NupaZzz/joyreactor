from bs4 import BeautifulSoup
import json

visited_links = set()

def get_links(user_id):
    with open(f'page_data_{user_id}.json', 'r', encoding='utf-8') as file:
        data = file.read()
    soup = BeautifulSoup(data, "html.parser")
    links_tags = {}
    for post in soup.find_all(class_='postContainer'):
        href = post.find(class_='link').get('href')
        if href not in visited_links:
            visited_links.add(href)
            taglist = post.find(class_='taglist').text
            links_tags[href] = {'tags': taglist}

    try:
        with open(f'{user_id}_links.json', 'r', encoding='utf-8') as file:
            saved_links = json.load(file)
    except FileNotFoundError:
        saved_links = {}

    for link in links_tags:
        if link not in saved_links:
            saved_links[link] = links_tags[link]

    with open(f'{user_id}_links.json', 'w', encoding='utf-8') as file:
        json.dump(saved_links, file, indent = 4, ensure_ascii=False)

    return links_tags

if __name__ == "__main__":
    get_links()