import csv
import json

with open('data/contracts.csv', 'r') as file:
	reader = csv.reader(file)
	group = 0

	output = []

	for row in reader:
		if group != 0 and row[3] > 1:
			output.append({
				'id': row[0],
				'group': group, 
				'label': row[1], 
				'level': 1
				})
			group += 1
	with open('data/base_nodes.js', 'w+') as file2:
		json.dump(output,file2)
