import requests


def test_ping():
    response = requests.get("http://0.0.0.0:8080/ping")
    status_code = response.status_code

    if (status_code == 200):
        print("ok")


if __name__ == '__main__':
    test_ping()
