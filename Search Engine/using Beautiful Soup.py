from bs4 import BeautifulSoup

def get_all_links(page):
	soup = BeautifulSoup(page)
	links = []
	for link in soup.find_all('a'):
		links.append(link.get('href'))
	return links