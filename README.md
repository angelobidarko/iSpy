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

Claude references: 
* `image_brightness` function, later used in `bg_im` to make sure scraped image is dark enough to hide embedded images. `bg_im` uses same mechanism as `scrape.py` from check-in. See below. 
* Changed treshold in `remove_white_background` to be variable instead of fixed. Function is more versatile
* Labeled parameters in all function defintions for clarity 

### `gameboard.jpg`: 
Contains randomly-pulled background image and 5 embedded images from `img_sized` folder. Updates every time user inputs a guess. 

### `img`: 
Folder of 10 images downloaded from the image, unedited. 

### `img_resized`: 
The folder containing images accessed in iSpy.py to embed into the background image. Images are created by `size_img.py`

### `size_img.py`: 
A script that accesses the image files in the `img` folder, resizes them to be 128 x 128 pixels, and saves them in a folder called img_sized. If img_sized does not exist, it creates the folder first.

Claude references: 
* Wrote the algebra in 'square' function 
* Used os to add the files to `img_sized` folder

### `hints.csv`: 
CSV file of 10 objects, their associated hints, and the name of the image file later accessed from `img_sized`

### `scrape.py`:
Original mechanism for getting a random image from https://randomwordgenerator.com/picture.php. Kept in repository for debugging purposes. Bypasses Cloudflare bot protection using Cloudscraper. 

Install: 
* pip install cloudscraper 
* pip install pillow 

References: 
* https://www.youtube.com/watch?v=G6K9C0JGxxs
* Claude: Accessed bytes of image from URL, saved those bytes to a temporary file called temp.jpg

### `scraped_image.jpg`: 
Output of either `scrape.py` or `iSpy.py`. Stores random image. Kept in repository for debugging purposes.
