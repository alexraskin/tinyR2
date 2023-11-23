import io
import os
import threading
from queue import Queue
from typing import Optional

import boto3
import tinify
from tqdm import tqdm

from config import Config

config: Config = Config()

class TinyR2:
    """
    TinyR2 compresses images using TinyPNG and Uploads them to R2 Cloudflare Storage

    :param key: TinyPNG API Key
    :param prefix: The prefix for the R2 Cloudflare Storage bucket
    :param r2_endpoint_url: The endpoint URL for R2 Cloudflare Storage
    :param r2_access_key: The access key for R2 Cloudflare Storage
    :param r2_secret_access_key: The secret access key for R2 Cloudflare Storage
    :param num_threads: The number of threads to use for uploading images to R2 Cloudflare Storage

    :return: None
    """

    def __init__(
        self,
        tinify_key: str,
        prefix: str,
        bucket_name: str,
        r2_endpoint_url: str,
        r2_access_key: str,
        r2_secret_access_key: str,
        num_threads: Optional[int] = 10,
    ) -> None:
        
        tinify.key: str = tinify_key
        self.prefix: str = prefix
        self.bucket_name: str = bucket_name
        self.images_path: str = os.path.join(os.getcwd(), "images")
        self.s3: boto3.client = boto3.client(
            "s3",
            endpoint_url=r2_endpoint_url,
            aws_access_key_id=r2_access_key,
            aws_secret_access_key=r2_secret_access_key,
        )
        self.num_threads: int = num_threads
        self._queue: Queue = Queue()
        self._threads: list = []
        self._setup_threads()

    def _setup_threads(self) -> None:
        """
        Sets up the threads for uploading images to R2 Cloudflare Storage

        :return: None
        """
        for _ in range(self.num_threads):
            t = threading.Thread(target=self._worker)
            t.start()
            self._threads.append(t)

    def _worker(self) -> None:
        """
        Worker function for uploading images to R2 Cloudflare Storage

        :return: None
        """
        while True:
            file_name = self._queue.get()
            if file_name is None:
                break
            buff = self._compress(file_name)
            self._upload(file_name, buff)
            self._remove(file_name)
            self._queue.task_done()

    def add_file(self, file_name: str) -> None:
        """
        Adds a file to the queue

        :param file_name: The name of the file to add to the queue

        :return: None
        """
        file_ext = ["jpg", "png", "jpeg", "webp"]
        if file_name.split(".")[1].lower() in file_ext:
            self._queue.put(file_name)
        else:
            print("Not a valid image format 🚨")
    
    def finish_uploading(self) -> None:
        """
        Finishes uploading all images to R2 Cloudflare Storage

        :return: None
        """
        self._queue.join()
        for _ in range(self.num_threads):
            self._queue.put(None)
        for t in self._threads:
            t.join()

    def _upload(self, filename: str, buff: bytes) -> bool:
        """
        Uploads the compressed image to R2 Cloudflare Storage

        :param filename: The name of the image to upload
        :param buff: The compressed image

        :return: True if the image was uploaded successfully, False otherwise
        """
        r2_file_path = f"{self.prefix}/{image.split('.')[0]}-optimized.jpg"
        try:
            self.s3.upload_fileobj(io.BytesIO(buff), self.bucket_name, r2_file_path)
        except Exception as e:
            print(f"🚨 Error uploading file: {e} | Exiting...")
            return False
        return True

    def _remove(self, image_name: str) -> bool:
        """
        Removes the original image from the images folder

        :param image_name: The name of the image to remove

        :return: True if the image was removed successfully, False otherwise
        """
        try:
            os.remove(os.path.join(self.images_path, image_name))
        except Exception as e:
            print(f"🚨 Error removing file: {e} | Exiting...")
            return False
        return True

    def _compress(self, image: str) -> bytes:
        """
        Uploads image to TinyPNG and then uploads the compressed image to R2 Cloudflare Storage

        :return: True if the image was compressed and uploaded successfully, False otherwise
        """
        try:
            source = tinify.from_file(os.path.join(self.images_path, image))
        except Exception as e:
            print(f"🚨 Error optimizing file: {e} | Exiting...")
            return False
        buff = source.to_buffer()
        return buff


if __name__ == "__main__":
    print("Starting TinyR2 🤖")

    client: TinyR2 = TinyR2(
          key=config.tinify_token,
          prefix=config.prefix,
          bucket_name=config.bucket_name,
          r2_endpoint_url=config.r2_endpoint_url,
          r2_access_key=config.r2_access_key,
          r2_secret_access_key=config.r2_secret_access_key,
      )

    for image in tqdm(client.images_path, desc="Compressing images and uploading to R2 Cloudflare Storage"):
        client.add_file(image)
        print(f"Added {image} to queue")
    client.finish_uploading()
    print("Finished TinyR2 🎉")