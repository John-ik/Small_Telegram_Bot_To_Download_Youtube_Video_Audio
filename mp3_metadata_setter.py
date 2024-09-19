import music_tag
import os
from PIL import Image


def set_mp3_image(name):
    print(name)
    files = os.listdir(name[:name.rfind("/")])
    for ext in ["jpg", "webp"]:
        name_with_ext = name[name.rfind("/") + 1:name.rfind(".") + 1] + ext
        if name_with_ext in files:
            file = music_tag.load_file(name)

            img = Image.open(name[:-3] + ext)

            k = max(img.size) / min(img.size)
            if min(img.size) == img.size[1]:
                img = img.resize((int(300 * k), 300))
            else:
                img = img.resize((300, int(300 * k)))

            new_img = Image.new("RGB", (300, 300), (255, 255, 255, 0))
            new_img.paste(img, (150 - img.size[0] // 2, 150 - img.size[1] // 2))
            new_img.save(name[:-3] + "png", "PNG")
            with open(name[:-3] + "png", "rb") as art_img:
                file["artwork"] = art_img.read()
            file.save()
            # os.remove(name[:-3] + "png")
            os.remove(name[:-3] + ext)
