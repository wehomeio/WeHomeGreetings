# -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import math

DRY_RUN = False

NAME_FILE = 'names.json'
NAME_TXT = 'names.txt'
OUTPUT_PATH = 'output'
INPUT_FILE = 'input/wehome-christmas.jpeg'
FONT = 'font/PingFang.ttc'
FONT_SIZE = 38

def edit_img(output_path, output_prefix, output_file_name, input_file, font, font_size, text_array, lon, lon_delta, dry_run=True):
  img = Image.open(input_file)
  width, height = img.size

  draw = ImageDraw.Draw(img)
  # 准备字体
  font = ImageFont.truetype(font, font_size)
  color = (231,192,155,1)

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
          text_array = [name, "粽有吉祥如意伴您左右"]
          edit_img(OUTPUT_PATH, prefix, text_array[0].encode("utf-8"), INPUT_FILE, FONT, FONT_SIZE, text_array, 1000, 10, DRY_RUN)
          print "Processed {}-{}".format(prefix, name.encode("utf-8"))
        names = set()
        prefix = raw_name.split("==")[1].strip().encode("utf-8")
        continue
      names.add(raw_name.strip().decode("utf-8"))
    ## last group
    for name in names:
      text_array = [name, "粽有吉祥如意伴您左右"]
      edit_img(OUTPUT_PATH, prefix, text_array[0].encode("utf-8"), INPUT_FILE, FONT, FONT_SIZE, text_array, 1000, 10, DRY_RUN)
      print "Processed {}-{}".format(prefix, name.encode("utf-8"))

if __name__ == "__main__":
  ## investment users
  name_set = set(parse_identity_json(NAME_FILE))
  for name in name_set:
    text_array = [name, "粽有吉祥如意伴您左右"]
    edit_img(OUTPUT_PATH, "VIP投资用户", text_array[0].encode("utf-8"), INPUT_FILE, FONT, FONT_SIZE, text_array, 1000, 10, DRY_RUN)
    print "Processed {}-{}".format("VIP投资用户", name.encode("utf-8"))

  ## other users
  process_normal_name_file(NAME_TXT)