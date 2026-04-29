import sys
import os
from PIL import Image

def square(input_path, size=128):
    with Image.open(input_path) as img:
        img = img.convert("RGBA")
        w, h = img.size
        min_dim = min(w, h)
        left = (w - min_dim) // 2
        top = (h - min_dim) // 2
        img = img.crop((left, top, left + min_dim, top + min_dim))
        resized = img.resize((size, size), Image.LANCZOS)
        return resized.convert("RGB")

def main():
    if len(sys.argv) == 1:
        imfile = 'img/' + input('Filename of input image: ')
    elif len(sys.argv) == 2:
        imfile = 'img/' + sys.argv[1]
    else:
        sys.exit("Usage: python3 size_img imagefile")

    os.makedirs('img_sized', exist_ok=True)
    name, ext = os.path.splitext(os.path.basename(imfile))
    output_path = os.path.join('img_sized', f"{name}_resized{ext}")

    resized = square(imfile)
    print(resized.size)
    resized.save(output_path)

if __name__ == '__main__':
    main()