**get.py**


get.py will create an output file called scraped_image.jpg (if one doesn't exist already) and save your image there.

How it works: 
Accesses the random image-generating website through its URL, bypassing using Cloudflare bot protection using Cloudscraper. 
Loads the JSON file that the site uses, containing all the images it "generates" when user clicks button. 
Turns file into dictionary, and picks a random background entry. For each entry, 5 of the **8 or 10** hidden images are randomly placed on the background with no overlap. 

**game_board.py**

This directory contains everything needed for
**iSpy** 

### `iSpy.py`: 
The game script. Players recieve hints about images steganographically hidden in a larger background image. They are allowed 4 guesses, inputted as strings in the terminal. If they run out of guesses, the hidden image is revealed with a white box around it to highlight the image. If they guess correctly within 4 plays, the photo is also revealed. 

Install: 
* pip install cloudscraper 
* pip install numpy
* pip install pillow 

To play: 
1. Run 'python3 iSpy.py' in terminal
2. Split screen with gameboard.jpg


### `img`: 
Folder of 10 images downloaded from the image, unedited. 

### `size_img.py`: 
A script that accesses the image files in the `img` folder, resizes them to be 128 x 128 pixels, and saves them in a folder called img_sized. If img_sized does not exist, it creates the folder first.

### `img_resized`: 
The folder containing images accessed in iSpy.py to embed into the background image. Images are created by `size_img.py`

### `hints.csv`: 
CSV file of 10 objects, their associated hints, and the name of the image file later accessed from `img_sized`

### `scrape.py`:
Original mechanism for getting a random image from https://randomwordgenerator.com/picture.php

References: 
* https://www.youtube.com/watch?v=G6K9C0JGxxs
* Claude: Wrote the contents of img_data in a file 