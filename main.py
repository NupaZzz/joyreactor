import requests
import json
import lxml
from bs4 import BeautifulSoup

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
}
url="https://reactor.cc/"

def get_url ():
    response=requests.get(url=url,headers=headers)
    soup=BeautifulSoup(response.text, "lxml")
    with open('page_data.json','w', encoding="utf-8")as file:
        file.write(str(soup))
        print("File created successfully.")

def get_links():
    with open('page_data.json', 'r', encoding='utf-8') as file:
        data=file.read()
    soup=BeautifulSoup(data, "lxml")  
    href_list = [] 
    for link_wr in soup.find_all(class_='link_wr'):
        for link in link_wr.find_all('a'):
            href = link.get('href')
            if href:
                href_list.append(href)
    return href_list

if __name__ == "__main__":
    get_url()
    links=get_links()
    for link in links:
        print("https://reactor.cc"+link)
