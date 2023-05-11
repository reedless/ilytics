from flask_cors import CORS
from flask import Flask, jsonify, request
from app_helpers import generate_unique_filename, delete_files, create_image_file,\
    read_and_encode_image, parse_image_data, parse_autocrop
import darknet
import autocrop
import json

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

    valid, data = parse_image_data(request)
    isAutoCrop = parse_autocrop(request)

    if not valid:
        error_code = 400  # Bad Request
        return data["error"], error_code

    input_file_path = data["filepath"]

    # Run autocrop is requested
    if isAutoCrop:
        try:
            autocrop.autocrop(input_file_path)
        except:
            isAutoCrop = False

    # Run the model
    stats = darknet.performDetect(imagePath=input_file_path, configPath="./aimodel/Crabbite_V2.cfg",
                                  weightPath="./aimodel/Crabbite_V2.weights", metaPath="./aimodel/Crabbite_V2.data")
    result_image_data = read_and_encode_image(result_filepath)

    # Cleanup
    delete_files(input_file_path, result_filepath)

    return jsonify(img=result_image_data, stat=stats, autocrop_completed=json.dumps(isAutoCrop))


if __name__ == '__main__':
    # predict()
    app.run(host='0.0.0.0', port=8080)
