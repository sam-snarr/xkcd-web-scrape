import requests
from bs4 import BeautifulSoup
import os

# should try and do this with multithreading

#print(__file__, os.path.basename(__file__))
dir_path = os.path.dirname(os.path.abspath( __file__ ))

url = 'https://xkcd.com/1'
os.makedirs('xkcd', exist_ok=True)
i = 1

while not url.endswith('#'):

	print('Getting image from '+str(i), url)

	# get the site
	site = requests.get(url)
	# exit the program if requests returns an error code
	site.raise_for_status()

	try:
		# read in the site as beautiful soup
		soup = BeautifulSoup(site.text, 'lxml')
		# select the component 
		img_element = soup.select('div#comic img')[0]
		# extract useful information
		title = img_element.get('title')
		alt_title = img_element.get('alt')
		src_url = img_element.get('src') # link

		# get image using src link
		img = requests.get('https:' + src_url)

		# write to xkcd folder with other images
		path = os.path.join('xkcd', str(i)+'--'+os.path.basename(src_url ))
		print('\tpath:' + path)
		file = open(path, 'wb')
		file.write(img.content)
		file.close()
	except:
		print('\t--there was an error with extracting image or writing it to file')

	# get the link of the next comic
	next_link = soup.select('a[rel="next"]')[0]
	url = 'https://xkcd.com' + next_link.get('href')

	# increment counter
	i+=1




