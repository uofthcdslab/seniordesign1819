import imageio, os
from PIL import Image, ImageFont, ImageDraw

inputDir = 'plots-dist/'
outputDir = 'gifs/'

font = ImageFont.truetype('sans-serif.ttf', 36)

if not os.path.exists(outputDir):
    os.makedirs(outputDir)

if not os.path.exists(outputDir):
    print('Plots directory', inputDir, 'not found')

# get all images in plots folder
images = os.listdir(inputDir)
groups = {}

# group into a set of lists organized by nature and time division
for img in images:
    parts = img.split('.')[0].split('-')
    group = parts[0] + '-' + parts[1]
    if len(parts) == 3:
        num = int(parts[2])
    elif len(parts) == 4:
        # special case for weeks
        week = parts[3]
        if len(week) == 1:
            week = '0' + week
        num = int(parts[2] + week)
    else:
        continue

    if group in groups:
        groups[group].append(num)
    else:
        groups[group] = [num]

def getImage(fname, g, num):
    img = Image.open(fname)
    draw = ImageDraw.Draw(img)
    draw.text((100, 150), g.upper().replace('-', ' ') + ' #' + str(num), (0, 0, 0), font=font)
    return img


# sort each list numerically and turn into a gif
for g in groups:
    print('Building:', g)
    groups[g].sort()
    images = []
    if groups[g][0] < 100:
        for num in groups[g]:
            images.append(getImage(inputDir + g + '-' + str(num) + '.png', g, num))
    else:
        # special case for weeks
        for num in groups[g]:
            images.append(getImage(inputDir + g + '-' + str(int(num/100)) + '-' + str(num%100) + '.png', g, num))
    imageio.mimsave(outputDir + g + '.gif', images)
