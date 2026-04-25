**get.py**
To run: 
python3 get.py

get.py will create an output file called scraped_image.jpg (if one doesn't exist already) and save your image there.

How it works: 
Accesses the random image-generating website through its URL, bypassing using Cloudflare bot protection using Cloudscraper. 
Loads the JSON file that the site uses, containing all the images it "generates" when user clicks button. 
Turns file into dictionary, and picks a random entry. 

**get2.py**

pip install nltk

pip install cloudscraper

python3 -c "import nltk; nltk.download('wordnet')"

pip install pillow

