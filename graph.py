import csv
import json

def write_csv(filename,nested_lst):
	with open(filename,"w") as file:
		writer = csv.writer(file)
		writer.writerows(nested_lst)

def get_contract_dict(filename):
	with open(filename,"r") as file:
		reader = csv.reader(file)
		# dict(addr:dict(edges:numtxns)) though the inner dict doesn't have anything yet
		return {row[0]:{} for row in reader}

def get_txns(filename):
	with open(filename,"r") as file:
		return json.load(file)

def make_graph():
	txns = get_txns("data/transactions.json")
	contracts = get_contract_dict("data/contracts.csv")
	for txn in txns:
		if txn[0] in contracts and txn[1] in contracts:
			if not txn[1] in contracts[txn[0]]:
				contracts[txn[0]][txn[1]] = 0
			if not txn[0] in contracts[txn[1]]:
				contracts[txn[1]][txn[0]] = 0
			contracts[txn[0]][txn[1]] += 1
			contracts[txn[1]][txn[0]] += 1
	
	contracts = {k: v for k, v in contracts.items() if v} # Only graph nodes with edges for now
	return contracts 

def generate_nodes():
	with open('data/contracts.csv', 'r') as file:
		reader = csv.reader(file)
		group = 0

		output = []

		for row in reader:
			if group != 0 and int(row[3]) > 1:
				output.append({
					'id': row[0],
					'group': group, 
					'label': row[1], 
					'level': 1
					})
			group += 1	
		with open('data/base_nodes.js', 'w+') as file2:
			json.dump(output,file2)



def generate_links(graph,filename):
	output = [] 
	for key, val in graph.items():
		for mapped_key,mapped_val in val.items():
			output.append({
				"target": key,
				"source": mapped_key,
				"strength": 0.1
			})
	with open(filename, "w+") as file:
		json.dump(output,file)




