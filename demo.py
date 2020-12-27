#!/usr/bin/env python

import os
import json
from multiprocessing.dummy import Pool as ThreadPool
import requests
from shutil import rmtree
import uuid

from tasks import FAKE_API_KEY
from tasks import FAKE_API_PORT

FILES_NUMBER = 10
FILE_SIZE = 1024 * 1  # 1024 = 1M

API_KEY = os.getenv('TEST_POC_API_KEY')
BASE_URI = os.getenv('BASE_URI') or f"http://localhost:{FAKE_API_PORT}/prod/poc"
REGION = 'us-east-1'
TEST_BUCKET = 'uniqnamedbucket5'
HEADERS = {'x-api-key': FAKE_API_KEY}


def create_temp_dir(where):
    full_path = os.path.realpath(where)
    directory = os.path.dirname(full_path) + '/tmp/'
    if os.path.isdir(directory):
        rmtree(directory)
    os.mkdir(directory)
    return directory


def generate_random_files(names):
    for file in names:
        with open(file, 'wb') as f:
            f.write(os.urandom(1024) * FILE_SIZE)


def create_test_bucket(bucket):
    data = json.dumps({"region": REGION, "bucket_name": bucket})
    uri = f"{BASE_URI}/create_s3_bucket"
    response = requests.request("POST", url=uri, headers=HEADERS, data=data)
    content = json.loads(response.content)
    return content


def upload_link(bucket_name):
    data = json.dumps({"bucket_name": bucket_name})
    uri = f"{BASE_URI}/upload_to_s3_bucket"
    response = requests.request("POST", url=uri, headers=HEADERS, data=data)
    content = json.loads(response.content)
    return content


def upload(test_file):
    url = upload_link(TEST_BUCKET)['upload_url']
    requests.request("PUT", url, data=open(test_file, "rb"))


def go_thread_pool(files):
    pool = ThreadPool(FILES_NUMBER)
    pool.map(upload, files)
    pool.close()
    pool.join()


if __name__ == "__main__":

    print(f">> HEADERS: {HEADERS}")
    print(f">> BASE_URI: {BASE_URI}")

    temp_dir = create_temp_dir(f"{uuid.uuid4().hex}_temp")
    random_names = [f"{temp_dir}/{uuid.uuid4().hex}" for x in range(FILES_NUMBER)]

    generate_random_files(random_names)
    create_test_bucket(TEST_BUCKET)
    go_thread_pool(random_names)

    if os.path.isdir(temp_dir):
        rmtree(temp_dir)
