import uuid
import os
import base64

error_messages = {"missing_image": "Missing required parameter: image. 'image' is base64 encoded image content",
                  "missing_filename": "Missing required parameter: filename."}


def create_image_file(imagedata, filepath):
    with open(filepath, "wb") as file:
        file.write(imagedata)
    return filepath


def generate_unique_filename(filename):
    random_hex = str(uuid.uuid4().hex)
    return random_hex + "_" + filename


def parse_json_request(request):
    data = request.get_json(force=True)
    if "image" not in data:
        return False, {"error": error_messages["missing_image"]}
    if "filename" not in data:
        return False, {"error": error_messages["missing_filename"]}
    decoded_image = base64.b64decode(data["image"])
    unique_filename = generate_unique_filename(data["filename"])
    final_filepath = create_image_file(decoded_image, unique_filename)

    return True, {"filepath": final_filepath}


def parse_form_request(request):
    if "image" not in request.files:
        return False, {"error": error_messages["missing_image"]}
    if "filename" not in request.form:
        return False, {"error": error_messages["missing_filename"]}

    unique_filename = generate_unique_filename(request.form["filename"])
    file = request.files['image']
    file.save(unique_filename)
    return True,  {"filepath": unique_filename}


def parse_request(request):
    if request.content_type.startswith('application/json'):
        return parse_json_request(request)
    if request.content_type.startswith('multipart/form-data'):
        return parse_form_request(request)

    return False, {"error": error_messages["wrong_content_type"]}


def delete_files(*filenames):
    '''
    Returns an array of boolean values. 
    True represents a successful delete
    False represents an unsuccessful delete
    '''
    out = []
    for filename in filenames:
        isDeleteSuccessful = False
        if os.path.exists(filename):
            try:
                os.remove(filename)
                isDeleteSuccessful = True
            except:
                # Do nothing
                pass

        out.append(isDeleteSuccessful)
    return out


def read_and_encode_image(filepath):
    with open(filepath, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        base64_string = encoded_string.decode('utf-8')

    return base64_string
