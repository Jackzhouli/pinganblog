# -*- coding:UTF-8 -*-
__autor__ = 'zhouli'
__date__ = '2019/9/3 23:01'
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import random
def validcode(request):
    validcode_str = ""

    def get_random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    img = Image.new("RGB", (280, 34), color=get_random_color())
    draw = ImageDraw.Draw(img)
    font_kwmo = ImageFont.truetype("static/cnblong/font/kumo.ttf", size=20)
    for i in range(5):
        random_num = str(random.randint(0, 9))
        random_alpha_low = chr(random.randint(95, 122))
        random_alpha_upper = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_alpha_low, random_alpha_upper])
        draw.text((i * 50, 5), random_char, get_random_color(), font=font_kwmo)
        validcode_str += random_char
    request.session["valid_code_str"] = validcode_str
    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()
    return data
