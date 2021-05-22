import os
from api import allowed_file
from werkzeug.utils import secure_filename

def handle_upload(file, dest, dest_len=None, save=True, return_img_path=False):
    if file == None:
        return {"detail": "File not found"}, 404

    if file.filename == '':
        return {"detail": "No image selected"}, 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename) # security purpose
        _, ext = os.path.splitext(filename) # take extension

        new_filename = f"{dest_len + 1}{ext}" # set new filename
        save_path = os.path.join(dest, new_filename)
        
        if save == True:
            file.save(save_path)

            if return_img_path == True:
                return {"saved": True}, save_path, 5211

            return {"saved": True}, 201
    else:
        return {"detail": "Filename not valid"}, 400
    return  {"saved": False}, 200