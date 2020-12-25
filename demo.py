import os
import json
from multiprocessing.dummy import Pool as ThreadPool
import requests
import uuid
from shutil import rmtree

FILES_NUMBER = 100


def create_temp_dir(where):
    full_path = os.path.realpath(where)
    directory = os.path.dirname(full_path) + '/tmp/'
    if os.path.isdir(directory):
        rmtree(directory)
    os.mkdir(directory)
    return directory


if __name__ == "__main__":
    API_KEY = os.getenv('TEST_POC_API_KEY')
    assert isinstance(API_KEY, str), ">> Please export appropriate TEST_POC_API_KEY"

    REGION = 'us-east-1'
    TEST_BUCKET = 'uniqnamedbucket5'

    BASE_URI = 'http://localhost:3000/prod/poc'
    HEADERS = {'x-api-key': API_KEY}

    temp_dir = create_temp_dir(f"{uuid.uuid4().hex}_temp")

    random_names = [f"{temp_dir}/{uuid.uuid4().hex}" for x in range(FILES_NUMBER)]

    for file in random_names:
        with open(file, 'wb') as f:
            f.write(os.urandom(1024) * 1024)

    def create_test_bucket():
        data = json.dumps({"region": REGION, "bucket_name": TEST_BUCKET})
        uri = f"{BASE_URI}/create_s3_bucket"
        response = requests.post(uri, headers=HEADERS, data=data)
        content = json.loads(response.content)
        return content

    def upload_link(bucket_name):
        data = json.dumps({"bucket_name": bucket_name})
        uri = f"{BASE_URI}/upload_to_s3_bucket"
        response = requests.post(uri, headers=HEADERS, data=data)
        content = json.loads(response.content)
        return content

    def upload_req(test_file):
        url = upload_link(TEST_BUCKET)['upload_url']
        requests.request("PUT", url, data=open(test_file, "rb"), headers=HEADERS)

    def go_thread_pool():
        pool = ThreadPool(FILES_NUMBER)
        pool.map(upload_req, random_names)
        pool.close()
        pool.join()

    create_test_bucket()
    go_thread_pool()
