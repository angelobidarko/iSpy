**get.py**

Python libraries to install:

pip install cloudscraper

pip install pillow

To run: 
python3 get.py

get.py will create an output file called scraped_image.jpg (if one doesn't exist already) and save your image there.

How it works: 
Accesses the random image-generating website through its URL, bypassing using Cloudflare bot protection using Cloudscraper. 
Loads the JSON file that the site uses, containing all the images it "generates" when user clicks button. 
Turns file into dictionary, and picks a random background entry. For each entry, 5 of the **8 or 10** hidden images are randomly placed on the background with no overlap. 

**game_board.py**

