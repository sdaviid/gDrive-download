import requests
import argparse
import os
from urllib.parse import urlparse

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
    save_response_content(response, destination)    




def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None




def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)



def handler_id(data):
    if data.startswith('http') == False:
        return data
    data_parse = urlparse(data)
    if data_parse.path.startswith('/file/d/') == False:
        return False
    return data_parse.path.split('/')[3]






if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="gdrive download")
    parser.add_argument('--id', type=str, required=True)
    parser.add_argument('--name', type=str, required=True)
    parser.add_argument('--path', type=str, required=False, default=os.getcwd())
    args = parser.parse_args()
    file_id = handler_id(args.id)
    destination = os.path.join(args.path, args.name)
    download_file_from_google_drive(file_id, destination)

