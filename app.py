from flask_cors import CORS
from flask import Flask, jsonify, request
from app_helpers import generate_unique_filename, delete_files, create_image_file,\
    read_and_encode_image, parse_request
import base64
import darknet

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)
stats = []


@app.route('/ping', methods=['GET'])
def ping():
    """
    Ping route for sanity check. Return with status code 200 if the server is up and running.

    Returns:
        JSON Dictionary -- Return a valid key value pair
    """
    return jsonify({'data': 'pong!'})


@app.route('/invocations', methods=['POST'])
def invocations():
    # Get data and parameters
    result_filepath = "result.jpg"

    valid, data = parse_request(request)

    if not valid:
        error_code = 400  # Bad Request
        return data["error"], error_code

    input_file_path = data["filepath"]

    # Run the model
    stats = darknet.performDetect(imagePath=input_file_path, configPath="./aimodel/Crabbite_V2.cfg",
                                  weightPath="./aimodel/Crabbite_V2.weights", metaPath="./aimodel/Crabbite_V2.data")
    result_image_data = read_and_encode_image(result_filepath)

    # Cleanup
    delete_files(input_file_path, result_filepath)

    return jsonify(img=result_image_data, stat=stats)


@app.route('/upload', methods=['POST'])
def uploadFile():
    """
    REST API endpoint for image inference

    Returns:
        JSON Dictionary -- Return a dictionary containing image in base64 format and statistics of the counts and classification of rotifers
    """
    file = request.files['file']
    auto_crop = int(request.form['auto_crop'])
    file.save("./test.jpg")

    if auto_crop == 1:
        autocrop.autocrop("./test.jpg")

    stats = darknet.performDetect(imagePath="./test.jpg", configPath="./yolo-obj.cfg",
                                  weightPath="./backup/yolo-obj_best.weights", metaPath="./data/obj.data")
    with open("result.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        base64_string = encoded_string.decode('utf-8')
    return jsonify(img=base64_string, stat=stats)


if __name__ == '__main__':
    # predict()
    app.run(host='0.0.0.0', port=8888)
