# contact.py
from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageDraw
import glob
import calendar
import json

YEAR = 2025

# a dictionary to convert the 3 letter month to a number
MONTH_TO_NUM = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}

def make_contact_sheet(fnames):
    """\
    Make a contact sheet from a group of filenames:

    fnames       A list of names of the image files
    
    ncols        Number of columns in the contact sheet
    nrows        Number of rows in the contact sheet
    photow       The width of the photo thumbs in pixels
    photoh       The height of the photo thumbs in pixels

    marl         The left margin in pixels
    mart         The top margin in pixels
    marr         The right margin in pixels
    marl         The left margin in pixels

    padding      The padding between images in pixels

    returns a PIL image object.
    """
    ncols = 12
    nrows = 31

    marl = 0
    marr = 0
    mart = 0
    marb = 0

    photow = photoh = 30
    padding = 10

    # Read in all images and resize appropriately
    imgs = []
    for ph in fnames:
        i = ImageOps.invert(Image.open(ph).resize((photow, photoh)))
        enhancer = ImageEnhance.Contrast(i)
        imgs.append(enhancer.enhance(1.2))

    # for fn in fnames:
    # imgs = [ImageOps.invert(Image.open(fn).resize((photow, photoh))) for fn in fnames]

    # Calculate the size of the output image, based on the
    #  photo thumb sizes, margins, and padding
    marw = marl + marr
    marh = mart + marb

    padw = (ncols - 1) * padding
    padh = (nrows - 1) * padding
    isize = (ncols * photow + marw + padw, nrows * photoh + marh + padh)

    # Create the new image. The background doesn't have to be white
    white = (255, 255, 255)
    inew = Image.new("RGB", isize, white)


    # this was meant to add a border to the new and full moons, but it doesn't work yet
    with open(f"mooninfo_{YEAR}.json", "r") as moonfile:
        mooninfo = json.load(moonfile)

    full_new_moons = {" ".join(hour['time'].split()[:2]):hour['phase'] for hour in mooninfo if hour['phase'] > 99.8 or hour['phase'] <= .2}

    print(full_new_moons)

    # moons = {}
    # for key in full_new_moons.keys():
    #     print(f"{key.split()[0]}")
    #     if f"{int(key.split()[0])-1:02.0f} {key.split()[1]}" in full_new_moons.keys():
    #         continue
    #     new_key = f"{int(key.split()[0])} {MONTH_TO_NUM[key.split()[1]]}"
    #     moons[key] = full_new_moons[key]

    # print(json.dumps(moons, indent=4))
    # Insert each thumb:

    for icol in range(12):
        _, days = calendar.monthrange(YEAR, icol + 1)
        for irow in range(days):
            left = marl + icol * (photow + padding)
            right = left + photow
            upper = mart + irow * (photoh + padding)
            lower = upper + photoh
            bbox = (left, upper, right, lower)
            try:
                img = imgs.pop(0)
            except:
                break
            # if f"{irow} {icol+1}" in moons.keys():
            #     # add a circle border to the image
            #     ellipse = ImageDraw.Draw(img)
            #     ellipse.ellipse((0, 0, 30, 30), fill=None, outline=(255, 0, 0), width=2)
            inew.paste(img, bbox)
    return inew



# find a way to grab all of the images with the YEAR in the filename
files = sorted(glob.glob("images/*.jpg"))

inew = make_contact_sheet(files)
print(f"{inew.height}x{inew.width}")
inew.save("moon.png")
