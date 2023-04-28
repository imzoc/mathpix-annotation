"""
This program sends requests to the Mathpix server.
"""

import glob
import json
import os
import sys
import time

import requests


def main():
    request_handler = RequestHandler()
    data = request_handler.take_3_images()
    request_handler.write_results_to_file_raw(data)


class RequestHandler:
    def __init__(self):
        with open("internal/zach/api-key.txt") as api_key_file:
            api_key = str(api_key_file.readline())

        self.url = "https://api.mathpix.com/v3/text"
        self.headers = {
            "app_id": "Zach's MathML requests",
            "app_key": api_key,
        }
        self.images = glob.glob(
            os.path.join("mathml-images/images_filtered", "*.png")
        )

    def get_date(self):
        return time.strftime(f"%m-%d-%Y", time.gmtime())

    def take_3_images(self):
        """Sends 3 POST requests via send_post_request."""
        return [
            self.send_post_request(image) for image in self.images[0:4]
        ]

    def send_post_request(self, image):
        """This function sends a post request with the image passed to it.
        It uses constants declared at the beginning of the script.
        """
        print("Sending POST request...")

        options_json = json.dumps(
            {
                "math_inline_delimiters": ["$", "$"],
                "rm_spaces": True,
                "formats": ["data", "html"],
                "data_options": {
                    "include_mathml": True,
                    "include_latex": True,
                },
            }
        )

        r = requests.post(
            self.url,
            files={"file": open(image, "rb")},
            data={"options_json": options_json},
            headers=self.headers,
        )
        result = json.dumps(r.json(), indent=4, sort_keys=True)
        return result

    def write_results_to_file_raw(self, results):
        """This function writes results to a file in the results/
        directory.
        """
        batch_number = 0
        for file in glob.glob("results/*.json"):
            if file.startswith("results/raw-" + self.get_date()):
                local_batch_number = int(
                    file.split("-")[-1].replace(".json", "")
                )
                if local_batch_number >= batch_number:
                    batch_number = local_batch_number + 1

        results_file_name = f"results/raw-{self.get_date()}-batch-{str(batch_number)}.json"
        with open(results_file_name, "w") as file:
            for result in results:
                file.write(result)


if __name__ == "__main__":
    main()
