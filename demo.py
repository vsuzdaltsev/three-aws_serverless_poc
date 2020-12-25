import os
import json
from multiprocessing.dummy import Pool as ThreadPool
import requests
from shutil import rmtree
import uuid

FILES_NUMBER = 10
FILE_SIZE = 1024 * 1  # 1024 = 1M


def create_temp_dir(where):
    full_path = os.path.realpath(where)
    directory = os.path.dirname(full_path) + '/tmp/'
    if os.path.isdir(directory):
        rmtree(directory)
    os.mkdir(directory)
    return directory


if __name__ == "__main__":
    API_KEY = os.getenv('TEST_POC_API_KEY') or "d41d8cd98f00b204e9800998ecf8427e"
    BASE_URI = os.getenv('BASE_URI') or 'http://localhost:3000/prod/poc'
    REGION = 'us-east-1'
    TEST_BUCKET = 'uniqnamedbucket5'
    HEADERS = {'x-api-key': API_KEY}

    print(f"!!!!!!!!!! >> HEADERS: {HEADERS}")

    def generate_random_files(names):
        for file in names:
            with open(file, 'wb') as f:
                f.write(os.urandom(1024) * FILE_SIZE)

    def create_test_bucket():
        data = json.dumps({"region": REGION, "bucket_name": TEST_BUCKET})
        uri = f"{BASE_URI}/create_s3_bucket"
        print(uri)
        response = requests.post(uri, headers=HEADERS, data=data)
        print(response.__dict__)
        content = json.loads(response.content)
        return content

    def upload_link(bucket_name):
        data = json.dumps({"bucket_name": bucket_name})
        uri = f"{BASE_URI}/upload_to_s3_bucket"
        response = requests.post(uri, headers=HEADERS, data=data)
        content = json.loads(response.content)
        return content

    def upload(test_file):
        url = upload_link(TEST_BUCKET)['upload_url']
        requests.request("PUT", url, data=open(test_file, "rb"))

    def go_thread_pool():
        pool = ThreadPool(FILES_NUMBER)
        pool.map(upload, random_names)
        pool.close()
        pool.join()

    temp_dir = create_temp_dir(f"{uuid.uuid4().hex}_temp")
    random_names = [f"{temp_dir}/{uuid.uuid4().hex}" for x in range(FILES_NUMBER)]

    generate_random_files(random_names)
    create_test_bucket()
    go_thread_pool()

    if os.path.isdir(temp_dir):
        rmtree(temp_dir)
