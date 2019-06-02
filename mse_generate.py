import requests
import json
import sys

MISSING_FILE_MSG = "Usage: python mse_generate.py <filename>"
RESULTS_FILE_NAME = "results.txt"
FINISHED_MSG = f"Finished! The formatted file is in {RESULTS_FILE_NAME}"

def templated_card(card):
	text = f"""
card:
	has styling: false
	notes: 
	time created: 2019-06-02 01:47:48
	time modified: 2019-06-02 01:50:10
	name: {card["name"]}
	casting cost: {card["cost"]}
	image:
	super type: <word-list-type>{card["type"]}</word-list-type>
	sub type: <word-list-race></word-list-race>
	rarity: rare
	rule text:
		{card["rule_text"]}		
	flavor text: <i-flavor>{card["flavor_text"]}</i-flavor>"""

	if all(card.get(key) is not None for key in ["power", "toughness"]):
		text += f"""
	power: {card["power"]}
	toughness: {card["toughness"]}"""

	text += f"""
	card code text: 
	illustrator:
		{card["artist"]}
	copyright: 
	image 2: 
	copyright 2: 
	copyright 3: 
	mainframe image: 
	mainframe image 2:"""
	return text

def gen_card(raw_info):
	return {
		"name": raw_info.get("name"),
		"cost": raw_info.get("manaCost", "").replace("{", "").replace("}", ""),
		"type": raw_info.get("type"),
		"rule_text": raw_info.get("text", "").replace("\n", "\n\t\t").replace("{", "").replace("}", ""),
		"flavor_text": raw_info.get("flavor") or "",
		"power": raw_info.get("power"),
		"toughness": raw_info.get("toughness"),
		"artist": raw_info.get("artist"),
	}

def get_card_info(name):
	response = requests.get(
		url="https://api.magicthegathering.io/v1/cards",
		params={
			"name": name
		}
	)
	if response.status_code != 200:
		return {}

	# If successful, assume first result is the valid one
	cards_info = json.loads(response.text)
	cards_info = cards_info.get("cards")
	if len(cards_info) == 0:
		return None

	raw_info = cards_info[0]
	parsed_card = gen_card(raw_info)
	return parsed_card

def gen_text(card_names):
	full_text = ""
	for card_name in card_names:
		print(f"Getting info for {card_name}")
		card_info = get_card_info(card_name)
		full_text += templated_card(card_info)
	return full_text


card_names = [
]

def read_names_from_file(filename):
	f = open(filename, "r")
	text = f.read()
	card_names = text.split("\n")
	return card_names


def write_to_file(filename, text):
	f = open(RESULTS_FILE_NAME, "w+")
	f.write(text)
	f.close()


def run():
	if len(sys.argv) == 1:
		print(MISSING_FILE_MSG)
		return
	card_names = read_names_from_file(sys.argv[1])
	print(card_names)
	text = gen_text(card_names)
	write_to_file(RESULTS_FILE_NAME, text)
	print(FINISHED_MSG)

if __name__ == "__main__":
	run()
