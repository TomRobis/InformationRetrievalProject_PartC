import csv
import pickle
from os import mkdir
from os.path import isdir

import requests
import zipfile
import re



def save_obj(obj, name, path = ""):  # todo NAOR
    """
    This function save an object as a pickle.
    :param obj: object to save
    :param name: name of the pickle file.
    :return: -
    """
    if path:
        with open(path +'\\' + name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    else:
        with open(path + name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name, path = ""):
    """
    This function will load a pickle file
    :param name: name of the pickle file
    :return: loaded pickle file
    """
    if path:
        with open(path +'\\'+ name + '.pkl', 'rb') as f:
            return pickle.load(f)
    else:
        with open(path + name + '.pkl', 'rb') as f:
            return pickle.load(f)


__fid_ptrn = re.compile("(?<=/folders/)([\w-]+)|(?<=%2Ffolders%2F)([\w-]+)|(?<=/file/d/)([\w-]+)|(?<=%2Ffile%2Fd%2F)([\w-]+)|(?<=id=)([\w-]+)|(?<=id%3D)([\w-]+)")
__gdrive_url = "https://docs.google.com/uc?export=download"
def download_file_from_google_drive(url, destination):
    m = __fid_ptrn.search(url)
    if m is None:
        raise ValueError(f'Could not identify google drive file id in {url}.')
    file_id = m.group()
    session = requests.Session()

    response = session.get(__gdrive_url, params = { 'id' : file_id }, stream = True)
    token = _get_confirm_token(response)

    if token:
        params = { 'id' : file_id, 'confirm' : token }
        response = session.get(__gdrive_url, params = params, stream = True)

    _save_response_content(response, destination)    

def _get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def _save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
        
def unzip_file(file_path, target_dir):
    with zipfile.ZipFile(file_path, 'r') as z:
        z.extractall(target_dir)



def get_dir_file(folder_name, file_name=''):  #todo os.join
    routing_string = ""
    if folder_name:
        routing_string = folder_name
        if file_name:
            routing_string += '\\' + str(file_name) + '.pkl'
    else:  # if folder name isn't received
        raise ValueError('folder_path not given when retrieving a directory')
    return routing_string



def create_parent_dir(path):
    if path:
        if not isdir(path):
            mkdir(path)


def read_from_txt_file(file_path):  # might change later, but right now only useful to queries file
    read_lines = []
    with open(file_path,encoding="utf8") as txt_file:
        for line in txt_file:
            read_lines.append(line[:-1])
    return read_lines



def write_answers_to_csv(answers_tuples,csv_path):
    with open(csv_path, 'w',newline='') as myfile:
        csv_writer = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        # csv_writer.writerow(['tweet_id','rank','query_number'])
        for row in answers_tuples:
            row = [row[0],row[4],row[5]]
            csv_writer.writerow(row)

