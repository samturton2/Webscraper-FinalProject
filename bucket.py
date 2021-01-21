import logging
import boto3
from botocore.exceptions import ClientError
import os
from config_manager import itjobswatch_home_page_url
from src.itjobswatch_html_readers.itjobswatch_home_page_top_30 import ItJobsWatchHomePageTop30
from src.csv_generators.top_30_csv_generator import Top30CSVGenerator
import requests

def create_bucket(bucket_name, region):

    # Create bucket
    try:
        if bucket_name is None:
            print("Please enter a bucket name")
            return False
        elif region is None:
            print("Please enter a region")
            return False
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

    except ClientError as e:
        logging.error(e)
  	#print("Error!")
        return False
    print("Successfully created bucket!")
    return True

def upload_file(file_name, bucket, object_name=None):
  """Upload a file to an S3 bucket
  :param file_name: File to upload
  :param bucket: Bucket to upload to
  :param object_name: S3 object name. If not specified then file_name is used
  :return: True if file was uploaded, else False
  """

  # If S3 object_name was not specified, use file_name
  if object_name is None:
      object_name = file_name

  # Upload the file
  s3_client = boto3.client('s3')
  try:
      response = s3_client.upload_file(file_name, bucket, object_name)
  except ClientError as e:
      logging.error(e)
      return False
  return True

# upload_file("ItJobsWatchTop30.csv","eng74-final-project-bucket")


#  def list_files(self, bucket):
  """
  Function to list files in a given S3 bucket
  """
#    bucket = input("Please enter the bucket name: ")

#    s3 = boto3.client('s3')
#    contents = []
#    for item in s3.list_objects(Bucket=bucket)['Contents']:
#        contents.append(item)

#    for i in contents:
#        print(i)

def download_file(bucket, file_name):
  """
  Function to download a given file from an S3 bucket
  """

  BUCKET_NAME = bucket  # replace with your bucket name
  KEY = file_name  # replace with your object key

  s3 = boto3.resource('s3')
  s3.Bucket(BUCKET_NAME).download_file(KEY, 'ITJobsWatchTop30.csv')


if __name__ == "__main__":
    live_response = requests.get("https://www.itjobswatch.co.uk/")

    if live_response.status_code:
        cwd=os.getcwd() +"/"
        top_30 = ItJobsWatchHomePageTop30(itjobswatch_home_page_url())
        Top30CSVGenerator().generate_top_30_csv(top_30.get_top_30_table_elements_into_array(),
                                                cwd, 'ItJobsWatchTop30test.csv',
                                                top_30.get_table_headers_array())

        upload_file("ItJobsWatchTop30test.csv", "eng74-final-project-bucket")
        download_file("eng74-final-project-bucket", "ItJobsWatchTop30test.csv")
    # # If not then just download the s3 bucket data
    else:
        download_file("eng74-final-project-bucket", "ItJobsWatchTop30.csv")
