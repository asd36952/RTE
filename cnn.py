import rdflib
import urllib
import json
from bs4 import BeautifulSoup

def scrapArticles(keyword):

	start=1
	while(True):
		url=urllib.request.urlopen('http://searchapp.cnn.com/search/query.jsp?page=1&npp=10&start='+
			str(start)+'&text='+
			keyword[0]+'%2B'+
			keyword[1]+'&type=all&bucket=true&sort=relevance&collection=STORIES%2C&csiID=csi2')
		articles=url.read().decode()
		url.close()
		articles=articles.split('\n')
		articles=''.join(articles)
		articles=articles.split('\r')
		for part in articles:
			if(part.find("""{"buckets":[""")!=-1):
				articles=part
		parsed_articles=json.loads(articles)
		metaResults=parsed_articles['metaResults']['all']
		for result in parsed_articles['results'][0]:
			article_link=result['url']
			article_title=result['title']
			article_url=urllib.request.urlopen(article_link)
			article=article_url.read()
			article_url.close()
			print(article)
			soup=BeautifulSoup(article)
			ps=soup.find_all('p','zn-body__paragraph')
			article_content=""
			for p in ps:
				if(p.cite!=None):
					p.cite.extract()
				article_content=article_content+p.text
			print(article_content)
			print("--------------------------------------------------------------")


			
		start=start+10
		if(start>metaResults):
			break

