import secrets, os
from PIL import Image
from flask import current_app

def save_picture(pic):
    random_hex=secrets.token_hex(4)
    _, f_ext=os.path.splitext(pic.filename)
    pic_fn=random_hex+f_ext
    pic_path=os.path.join(current_app.root_path,'static\\DPs',pic_fn)
    new_size=(125,125)
    newimg=Image.open(pic)
    newimg.thumbnail(new_size)
    newimg.save(pic_path)
    return pic_fn