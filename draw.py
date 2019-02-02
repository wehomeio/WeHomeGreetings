# -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import math

DRY_RUN = False

NAME_TXT = 'names.txt'
OUTPUT_PATH = 'output'
INPUT_FILE = 'input/zombie.jpg'
FONT = 'font/Libian.ttc'
FONT_SIZE = 48
LONGITUDE = 1000
COLOR =(255,255,255,1)

def edit_img(output_path, output_prefix, output_file_name, input_file, font, font_size, text_array, lon, lon_delta, dry_run=True):
  img = Image.open(input_file)
  width, height = img.size

  draw = ImageDraw.Draw(img)
  # 准备字体
  font = ImageFont.truetype(font, font_size)
  color = COLOR

  for text in text_array:
    unicode_text = text
    if not isinstance(text, unicode):
      unicode_text = unicode(text,'UTF-8')

    text_width, text_height = font.getsize(unicode_text)  
    # place in middle
    lat = (width - text_width) / 2   
    draw_img(draw, lat, lon, unicode_text, font, color)
    # move to next line
    lon += text_height + lon_delta

  output_file = "{}/{}-{}.jpg".format(output_path, output_prefix, output_file_name)
  if not dry_run:
    img.save(output_file)
  return img

def draw_img(draw, lat, lon, text, font, color):
  draw.text((lat, lon), text, font=font, fill=color)

def parse_identity_json(input_file):
  import json
  with open(input_file) as data_file:    
    data = json.load(data_file)
  names = [d["name"] for d in data ]
  return names

def process_normal_name_file(filename):
  with open(filename) as f:
    raw_names = f.readlines()
    names = set()
    prefix = ''
    for raw_name in raw_names:
      if not raw_name.strip():
        continue
      if "==" in raw_name:
        for name in names:
          text_array = [name]
          edit_img(OUTPUT_PATH, prefix, text_array[0].encode("utf-8"), INPUT_FILE, FONT, FONT_SIZE, text_array, LONGITUDE, 10, DRY_RUN)
          print "Processed {}-{}".format(prefix, name.encode("utf-8"))
        names = set()
        prefix = raw_name.split("==")[1].strip()
        continue
      names.add(raw_name.strip().decode("utf-8"))
    ## last group
    for name in names:
      text_array = [name]
      edit_img(OUTPUT_PATH, prefix, text_array[0].encode("utf-8"), INPUT_FILE, FONT, FONT_SIZE, text_array, LONGITUDE, 10, DRY_RUN)
      print "Processed {}-{}".format(prefix, name.encode("utf-8"))

if __name__ == "__main__":
  ## other users
  process_normal_name_file(NAME_TXT)