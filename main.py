import requests
import json
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
		card_info = get_card_info(card_name)
		full_text += templated_card(card_info)
	print(full_text)


card_names = [
	"Blast Zone",
	"Pact of Negation",
	"Spellskite",
	"Vesuva",
	"City of Brass",
	"Gavony Township",
	"Godless Shrine",
	"Magus of the Moon",
	"Nykthos, Shrine to Nyx",
	"Remorseful Cleric",
	"Shalai, Voice of Plenty",
	"Thragtusk",
	"Venser, Shaper Savant",
	"Viscera Seer",
	"Walking Ballista",
	"Westvale Abbey",
	"Coalition Relic",
	"Pyromancer Ascension",
	"Wurmcoil Engine",
	"Abrade",
	"Abrupt Decay",
	"Birds of Paradise",
	"Dismember",
	"Duskwatch Recruiter",
	"Ezuri, Renegade Leader",
	"Knight of Autumn",
	"Pyretic Ritual",
	"Animation Module",
	"Horizon Canopy",
	"Oblivion Stone",
	"Relic of Progenitus",
	"Steam Vents",
	"Tolaria West",
	"Anafenza, the Foremost",
	"Blooming Marsh",
	"Grove of the Burnwillows",
	"Legion Warboss",
	"The Rack",
	"Amulet of Vigor",
	"Ancient Stirrings",
	"Chromatic Star",
	"Expedition Map",
	"Gemstone Mine",
	"Serum Visions",
	"Spirebluff Canal",
	"Summoner's Pact",
	"Welding Jar",
	"Chord of Calling",
	"Concealed Courtyard",
	"Desperate Ritual",
	"Devoted Druid",
	"Elvish Archdruid",
	"Elvish Clancaller",
	"Eternal Witness",
	"Gilt-Leaf Palace",
	"Heritage Druid",
	"Kitchen Finks",
	"Knight of Autumn",
	"Path to Exile",
	"Rattlechains",
	"Restoration Angel",
	"Terminus",
	"Urborg, Tomb of Yawgmoth",
	"Vizier of Remedies",
	"Wall of Omens",
	"Wilt-Leaf Liege",
]
gen_text(card_names)
