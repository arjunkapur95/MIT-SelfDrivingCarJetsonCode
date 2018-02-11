# source /home/cs231n/myVE35/bin/activate

import requests

def download_file_from_google_drive(id, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    


# download_file_from_google_drive('0B7eQasUpbyfZb04zZ3hJa09yRVk', 'z2.zip')
# download_file_from_google_drive('0B7eQasUpbyfZRENtaE9HeEVzVUE', 'z3.zip')
# download_file_from_google_drive('0B7eQasUpbyfZaFYxUXpzanJOQkU', 'z4.zip')
# download_file_from_google_drive('0B7eQasUpbyfZTExzX1BvVkRlczA', 'z5.zip')
# download_file_from_google_drive('0B7eQasUpbyfZT1ExVXY3bFlKWWs', 'z6.zip')
download_file_from_google_drive('0B0OrXzyTLfIiUGhCQ2xfWHhhWGM', 'full.zip')

# import os
# directory='full_unzipped'
# if not os.path.exists(directory):
#     os.makedirs(directory)

# import zipfile
# zip_ref = zipfile.ZipFile('half_dataset_stuff/full.zip', 'r')
# zip_ref.extractall(directory)
# zip_ref.close()