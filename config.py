import os
from dotenv import load_dotenv

load_dotenv()

class Config:
  """
  Config is a class that holds the configuration for TinyR2

  :param tinify_token: TinyPNG API Key
  :param prefix: The prefix for the R2 Cloudflare Storage bucket
  :param r2_endpoint_url: The endpoint URL for R2 Cloudflare Storage
  :param r2_access_key: The access key for R2 Cloudflare Storage
  :param r2_secret_access_key: The secret access key for R2 Cloudflare Storage
  :param num_threads: The number of threads to use for uploading images to R2 Cloudflare Storage

  :return: None
  """
  def __init__(self):
    self.tinify_token: str = os.getenv("TINIFY_TOKEN")
    self.prefix: str = os.getenv("PREFIX")
    self.bucket_name: str = os.getenv("BUCKET_NAME")
    self.r2_endpoint_url: str = os.getenv("R2_ENDPOINT_URL")
    self.r2_access_key: str = os.getenv("R2_ACCESS_KEY_ID")
    self.r2_secret_access_key: str = os.getenv("R2_SECRET_ACCESS_KEY")
    self.num_threads: int = 10
