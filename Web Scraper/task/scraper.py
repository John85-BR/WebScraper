import requests
import os
from bs4 import BeautifulSoup

numberPages = int(input())
typeArticles = input()
count = 1

for i in range(1,numberPages+1):
    new_dir = "Page_" + str(i)
    os.mkdir(new_dir)


while count <= numberPages:



    url = "https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&year=2020&page=" + str(
        count)  # "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3"  # input("Input the URL:")
    response = requests.get(url)

    if response.content and response.status_code in range(200, 299):
        soup = BeautifulSoup(response.content, 'html.parser')
        article = soup.find_all('article')

        tail = []
        for i in article:
            type = i.find('span', class_="c-meta__type")
            if type.text == typeArticles:
                a = i.find('a', {'data-track-action': 'view article'})
                tail.append(a.get('href'))
        url2 = []

        for i in tail:
            url2.append("https://www.nature.com" + i)

        for i in url2:
            response2 = requests.get(i, headers={'Accept-Language': 'en-US,en;q=0.5'})
            soup2 = BeautifulSoup(response2.content, 'html.parser')
            title = soup2.title.text.replace(' ', '_').replace(':', '').replace('?', '')
            print(title)

            body = None
            if soup2.find('p', {"class": "article__teaser"}) is None:
                body = soup2.find('div', {"class": "c-article-body main-content"})
            else:
                body = soup2.find('p', {"class": "article__teaser"})

            print(body.text.replace('\n', ''))


            file = open(f'Page_{count}/{title}.txt', 'wb')
            file.write(body.text.encode())
            file.close()
            print(f"Content saved.")

    else:
        print("Invalid page!")
        print(f"The URL returned {response.status_code}!")
        break

    count += 1
if count == numberPages:
    print("Saved all articles.")
