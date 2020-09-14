import pandas as pd
import gspread
from df2gspread import gspread2df as g2d
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/spreadsheets']

def readFromGoogle(SPREADSHEET_KEY, WORKSHEET_NAME):
	credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
	gc = gspread.authorize(credentials)
	urls = g2d.download(SPREADSHEET_KEY, WORKSHEET_NAME,credentials=credentials, col_names = True)

	print("Reading done")
	return urls[['Ticker', 'Company']]