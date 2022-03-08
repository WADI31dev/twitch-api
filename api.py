from google.cloud import storage

import pandas as pd

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from twitch import twitch

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


def download_blob(bucket_name, blob_name, file_name):

    client = storage.Client()  # verifies $GOOGLE_APPLICATION_CREDENTIALS
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(file_name)


def upload_file(bucket_name, file_name, blob_name):

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(file_name)


@app.get("/{twitcher}")
def index(twitcher):

    # download twitcher stats
    bucket_name = "le-wagon-data"
    blob_name = f"twitchers/{twitcher}.csv"
    file_name = f"{twitcher}.csv"

    #download_blob(bucket_name, blob_name, file_name)

    # read stats
    #df = pd.read_csv(file_name)
    # direct read from pandas
    #csv_url = f"gs://le-wagon-data/twitchers/{twitcher}.csv"

    #df2 = pd.read_csv(csv_url)

    stats = twitch(twitcher)

    return {f'{twitcher}': stats}
    #return {"key": "value"}
