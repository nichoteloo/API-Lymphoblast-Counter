import os
from api import allowed_file
from werkzeug.utils import secure_filename

def handle_upload(file, dest, save=True, return_img_path=False):
    """
    func: image handling
    input: file, destination folder, amount of dir in destination folder, save condition, return img path condition
    output: json, detail saved or not
    """
    if file == None:
        return {"detail": "File not found"}, 404

    if file.filename == '':
        return {"detail": "No image selected"}, 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename) # security purpose
        save_path = os.path.join(dest, f"{filename}")

        if save == True:
            file.save(save_path)

            if return_img_path == True:
                return {"saved": True, "save_path":save_path}, 201

            return {"saved": True}, 201
    else:
        return {"detail": "Filename not valid"}, 400
    return  {"saved": False}, 200