from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

urls = ("http://www.mayo-clinic-jobs.com/go/Information-Technology%2C-Engineering-and-Architecture-Jobs/255296/?q=&sortColumn=referencedate&sortDirection=desc", "http://www.mayo-clinic-jobs.com/go/Information-Technology%2C-Engineering-and-Architecture-Jobs/255296/25/?q=&sortColumn=referencedate&sortDirection=desc")
 
out = open('output.csv', 'w', newline='')
wr = csv.writer(out, dialect='excel')
wr.writerow(['Date', 'Job Title', 'Location', 'Facility', 'Description', 'Qualifications'])

for url in urls:
	soup = BeautifulSoup(urlopen(url),'html.parser')
	table = soup.find(id ="searchresults").tbody('tr')
	for entry in table:
		# -- cut the relevant info out of each table entry
		link = 'http://www.mayo-clinic-jobs.com{0}'.format(entry.select(".jobTitle > a")[0]['href'])
		title = entry.select(".jobTitle > a")[0].string
		date = entry.select(".jobDate")[0].string.strip()
		location = entry.select(".jobLocation")[0].string
		facility = entry.select(".jobFacility")[0].string

		# -- follow the link to get the description
		soup_descrip = BeautifulSoup(urlopen(link), 'html.parser')

		# -- process the text after bold section texts we want via string splitting
		# --- have to encode the input as ascii otherwise you get invalid encode errors
		text = ' '.join(soup_descrip.find(class_='job').find(string="Job Description").parent.parent.strings).encode('ascii', 'ignore')

		# --- yucky string splitting on headers
		start_str = text.find('Job Description'.encode('utf-8')) + len('Job Description')
		split_str_start = text.find('Basic Qualifications:'.encode('utf-8'))
		split_str_end = split_str_start + len('Basic Qualifications:')
		end_str = text.find('Other Qualifications:'.encode('utf-8'))

		description = text[start_str:split_str_start:]
		quals = text[split_str_end:end_str:]

		wr.writerow([date, '=HYPERLINK("{0}","{1}")'.format(link, title), location, facility, description.decode('utf-8'), quals.decode('utf-8')])

