import os 
from  dotenv import load_dotenv
from google.cloud import storage

load_dotenv()

GOOGLE_CLOUD_PROJECT=os.getenv('GOOGLE_CLOUD_PROJECT')
if not GOOGLE_CLOUD_PROJECT: 
    raise "Google Cloud Project has'nt been set in the environment variables." 

BUCKET=os.getenv("BUCKET")
if not BUCKET: 
    raise "Google GCS Bucket not specified in env"

DIR="sounds"

async def upload_to_bucket(local_file_path, blob_name):
    storage_client = storage.Client(project=GOOGLE_CLOUD_PROJECT)  # Your project ID
    bucket = storage_client.bucket(BUCKET)

    try: 
        blob = bucket.blob(f"{DIR}/{blob_name}")  # Simple object name

        blob.upload_from_filename(local_file_path)
        print("Test upload successful")

        gcs_uri = f"gs://{BUCKET}/{DIR}/{blob_name}"
        return gcs_uri

    except Exception as e: 
        raise f"Encountered an error while uplaoding to Bucket: {str(e)}"
