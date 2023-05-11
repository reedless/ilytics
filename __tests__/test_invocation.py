import requests
import base64

test_image_location = "test_img.jpg"
target_url = "http://0.0.0.0:8080/invocations"


def test_json():
    with open(test_image_location, "rb") as test_img:
        encoded_data = base64.b64encode(test_img.read())
        encoded_string = encoded_data.decode("utf-8")

    payload = {"image": encoded_string, "filename": test_image_location}

    response = requests.post(target_url, json=payload)

    if response.status_code == 200:
        print("application/json ok")


def test_multiform():
    # https://requests.readthedocs.io/en/latest/user/quickstart/#post-a-multipart-encoded-file
    file = open(test_image_location, "rb")
    payload = {"image": (test_image_location, file),
               "filename": (None, test_image_location)}

    response = requests.post(target_url, files=payload)

    if response.status_code == 200:
        print("multipart/form-data ok")


if __name__ == '__main__':
    test_json()
    test_multiform()
