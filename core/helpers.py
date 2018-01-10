import re

def process_sheet_data(sheet_data):
	print("PROCESSING SHEET DATA")
	data = {
		'endpoints': dict(),
		'corpora': dict(),
		'tables': dict()
	}
	sheets = sheet_data['sheets']
	for sheet in sheets:
		sheet_title = sheet['properties']['title'].strip().lower()
		rows = sheet['data'][0]['rowData']
		for i in range(0, len(rows)):
			values = rows[i].get('values', [])
			for j in range(0, len(values)):
				value = values[j].get('formattedValue', None)
				header = rows[0]['values'][j].get('formattedValue', None)
				if sheet_title == 'endpoints':
					if header and header not in data['endpoints']:
						data['endpoints'][header] = []
					elif value and header and header in data['endpoints']:
						data['endpoints'][header].append(value)
				elif sheet_title == 'corpora':
					if header and header not in data['corpora']:
						data['corpora'][header] = []
					elif value and header and header in data['corpora']:
						data['corpora'][header].append(value)
				else:
					if header and header not in data['tables']:
						data['tables'][header] = []
					elif value and header and header in data['tables']:
						data['tables'][header].append(value)
	for key in data['endpoints']:
		values = list(filter(None, data['endpoints'][key]))
		data['endpoints'][key] = "\n".join(values)
	return data

def parse_sheet_url(url):
	exp = re.compile('/spreadsheets/d/([a-zA-Z0-9-_]+)')
	m = exp.search(url).group()
	if m:
		return m[16:]
	else:
		return None