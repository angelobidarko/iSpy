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

This directory contains everything needed for
**Chapter 8 (What is My Problem?)** 

`erase32.py`: Starter code for instructors who want to complete ALE 8.2 in class with the students.

`pair32.py`: A script that allows a student to compare two colored blocks that differ by a small `adjustment` (i.e., a few bits in the encoding space). It helps the students to understand that there's more detail in an image than the human eye can discern.

`images/photobomb[1-3].jpg`: Three images of Waldo moving through Harvard Yard. We'd like the picture of the Yard with Waldo removed.  We created this sequence of pictures by copying a single picture of Harvard Yard and then inserting Waldo in three different locations.

`images/photobomb-mode.jpg`: The result of a version of the `ale01` script that uses `statistics.mode` instead of `statistics.median`.  It looks good, right?

`images/duck[1-3]*.jpg`: Three images of a common background and an object (the CS50 ddb duck) that we'd like to eliminated.  This is a real sequence of three pictures, and as such, even the pixels where the duck isn't even placed are subtly different from picture to picture. The images come in both black-and-white and color.

`images/duck-mode.jpg`: The result of a version of the `ale01` script that uses `statistics.mode` instead of `statistics.median`.  It does NOT look good! Your answer to ALE #1, step 7 will explain why.

`images/apsu[1-6].jpg`: Seven actual images of a common background and a person who we'd like to remove from the picture.  The unintended subject overlaps himself in any three of these pictures, and thus we need more than three pictures to completely remove him.  Thanks again to John Nicholson, from whose original assignment we got these pictures.

`zero.py`: Script illustrating the clearing of the lowest 4 bits in each channel of the pixels in an image.

`images/harvard.png`: The original image of Harvard Yard without Waldo photobombing it. I didn't take this picture.

`images/garden*.png`: The original image of the Boston Public Garden without Waldo photobombing it. I took this picture. This image comes in both black-and-white and color.

`xverse.py`: A script that uses simple modifications to images to illustrate different traversals of 2-dimensional data.

`ale02.py`: The starter code for ALE 8.2.  Its code contents are the same as ALE #5 from Chapter 6.

`ale04.py`: The starter code for ALE 8.4.

`create_gif.py`: Code for a possible ALE at some point in the future. Right now it just creates a GIF from a collection of similarly named images.
