# mse-importer
Small tool to import cards into Magic Set Editor

## Requirements
This tool requires Python 3
In order to manipulate `.mse-set` files I recommend using 7z: https://www.7-zip.org/download.html  

## How to use it
First generate the content of the set file:
- Store the list of cards you want to import in a txt file, one card name per line.
- Open a command line and run  `python mse_generate.py <filename>.txt `
. Wait until the program finishes
- The formatted file will be in `result.txt`

Now we need to add that to an MSE Set:
- Go to the folder where your MSE set save file  is located(If you don't have one, create one and add an empty card)
- Using 7z right-click and select 'Open archive'
- Find the `set` file, right-click -> Edit (with notepad)
- Paste the full content of `result.txt` at the bottom, on a new line before `version control`
- Save and close, 7z will ask to change, select OK
- Open MSE and Load your set, your cards should be there, enjoy!

## TODO
Create an MSE Set instead of having to do the manual steps
Specify a full set directly
Allow Multiverse ID's
