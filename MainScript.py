from requests_html import HTMLSession
import pandas as pd
import schedule
import time
from ReadFromGoogle import readFromGoogle
from UpdateData import update
from WriteToGoogle import write

SPREADSHEET_KEY = '1PfDAquK5ioQuWAvK4ujhenN5aqlBBKTRJTOqRmneH_Q'
WORKSHEET_NAME = 'Testing'

def main():
	data = {'Company':[],
		'Year': [],
		'Links': [],
		'LinkLabel': [],
		'LinkInfo': []
		}

	df = pd.DataFrame(data)
	dfJSON = []

	dfREAD = readFromGoogle(SPREADSHEET_KEY, WORKSHEET_NAME)
	urls = dfREAD['Company'].to_list()

	for url in urls: 
		#ADD MORE YEARS HERE BY CALLING main BY PASSING THE YEAR AS A STRING
		try:
			df = update(df, url, "2020")
			df = update(df, url, "2019")
			df = update(df, url, "2018")
			df = update(df, url, "2017")
		except Exception as e:
			print(e, url)
		dfJSON.append(df[['Year', 'Links','LinkLabel', 'LinkInfo']].to_json(orient="records"))
		df = pd.DataFrame(data)

	print("Updated")
	dfREAD['Results in JSON'] = dfJSON
	newLinks = []
	for link in dfREAD['Results in JSON']:
		newLinks.append(link.replace('\\/', '/').replace('//', '/').replace('https:/', 'https://'))
	dfREAD['Results in JSON'] = newLinks
	write(dfREAD, SPREADSHEET_KEY, WORKSHEET_NAME)

# main()

# IF YOU WANT TO TEST IT, COMMENT THE BELOW SECTION AND UNCOMMENT THE ABOVE MAIN() CALL

schedule.every().day.do(main)
while 1:
	schedule.run_pending()
	time.sleep(1)
