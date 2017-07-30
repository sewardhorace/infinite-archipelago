import os, json
import gspread
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession

scope = ['https://spreadsheets.google.com/feeds']
creds = Credentials.from_service_account_file('credentials/Infinite Labyrinth-110752903121.json', scopes=scope)

# https://coreyward.svbtle.com/how-to-send-a-multiline-file-to-heroku-config

client = gspread.Client(auth=creds)
client.session = AuthorizedSession(creds)

workbook = client.open('Labyrinth')
worksheets = [
	'General',
	'Rooms',
	'Characters',
	'Objects',
	'Magic',
	'Seafaring'
]

data = {}

for worksheet in worksheets:
	sheet = workbook.worksheet(worksheet)

	headers = sheet.row_values(1)
	header_count = len(list(filter(None, headers)))

	for i in range(header_count):
		values = sheet.col_values(i+1)
		values = list(filter(None, values))

		key = values[0]
		print("writing " + key + "...")
		data[key] = values[1:]
	
with open('core/input_data/data.json', 'w') as f:
	json.dump(data, f)