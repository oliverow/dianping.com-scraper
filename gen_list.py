from bs4 import BeautifulSoup

#searchPage = 'https://www.dianping.com/search/keyword/2/0_%E5%87%91%E5%87%91'
#page = requests.get(searchPage).content
page = open('web.html')
soup = BeautifulSoup(page)

lst = soup.find('div', attrs={'class': 'shop-all-list'}).find('ul').findChildren('li')
with open('list.txt', 'w+') as file:
    for i in range(len(lst)):
        file.write(lst[i].div.img['title'].replace(' ', '') + ' ' + lst[i].div.a['href'] + '\n')
