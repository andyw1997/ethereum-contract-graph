import re
import urllib.request
from bs4 import BeautifulSoup
import requests
import csv
import json

headers = {'Accept-Encoding': 'identity'}
base_url = "https://etherscan.io/contractsVerified/{0}"
code_url = "https://etherscan.io{0}"

def write_csv(filename,nested_lst):
	with open(filename,"w") as file:
		writer = csv.writer(file)
		writer.writerows(nested_lst)


# Generate top 1000 contracts in chunks of 25 (41 times) 
def pull_data():
	# Headers for CSV 
	# final = [["Rank","Address","Balance","Percentage","TxCount","Relative Path","Source Code(URL TEMP)"]]
	final = [["Address","ContractName","Balance","TxCount"]]
	page = 1
	while True:
		print ("page " + str(page))
		url = base_url.format(page)
		# html = urllib.request.urlopen(url).read()
		html = requests.get(url, auth=('user','pass'))
		bs = BeautifulSoup(html.text,"lxml")
		tbl = bs.findAll('table')[0]
		# Parse the href from the table (could be resolved in BS4)
		href_match_pattern = r'href=[\'"]?([^\'" >]+)'
		
		#removed url: [re.search(href_match_pattern,str(url.a)).group(0)[6:] for url in tr.findAll("td") if url.a]
		output = []
		for tr in tbl.findAll('tr'):
			output.append([td for td in tr.findAll("td")])

		# Delete empty cells
		output = [[x[0], x[1], x[3], x[4]] for x in output if x]
		if len(output) == 0:
			break;

		# Strip unnecessary characters out and print cleanly
		for i in range(len(output)):
			output[i] = [str(x).replace("<td>","").replace("</td>","").replace('<font color=\'orange\' size=2><i title=\'Verified Code\' class="fa fa-check-circle-o"></i></font>',"") \
				.replace('class="fa fa-check-circle-o"', "").replace("Ether", "").replace("<b>","").replace("</b>","") for x in output[i]]
			output[i][0] = (re.findall("<a.*?>(.*)</a>",output[i][0])[0])

		output = [x for x in output if int(x[3]) > 2] #remove contracts that are just isolated
		final.extend(output)
		page += 1
	write_csv("data/contracts.csv",final)

pull_data();