# -*- coding: utf-8 -*-
from flask import render_template, Flask, request, send_file
from draw import edit_img, INPUT_FILE, FONT, FONT_SIZE
import StringIO
import logging

app = Flask(__name__)

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
app.logger.addHandler(handler)
app.logger.handlers.extend(logging.getLogger("project-zombie.log").handlers)

logger = app.logger

@app.route('/', methods=['GET', 'POST'])
def generate_zombie():
  if request.method == 'GET':
    logger.error("Browser is {}".format(request.user_agent.browser))
    logger.error("uas is {}".format(request.user_agent.string))
    logger.error("platform is {}".format(request.user_agent.platform))
    return render_template('index.html')
  elif request.method == 'POST':
    name = request.form.get('name').strip()
    logger.error("Sent love to {}".format(name.encode('utf-8')))
    text_array = [name]
    img = edit_img('tmp', "tmp", text_array[0].encode("utf-8"), INPUT_FILE, FONT, FONT_SIZE, text_array, 350, 10, True)
    img_io = StringIO.StringIO()
    img.save(img_io, 'JPEG', quality=100)
    img_io.seek(0)
    # adjustment for iOS
    as_attachment = False
    if request.user_agent.platform == "iphone":
      as_attachment = True
    return send_file(img_io, attachment_filename='wehome.jpg', as_attachment=as_attachment)


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)