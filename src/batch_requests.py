"""
This program sends requests to the Mathpix server.
"""

import glob
import json
import os
import sys
import time

import requests


class BatchRequestHandler:
    def __init__(self):
        with open("internal/zach/api-key.txt") as api_key_file:
            api_key = str(api_key_file.readline())
        self.url = "https://api.mathpix.com/v3/batch"

        self.headers = {
            "app_id": "Zach's MathML requests",
            "app_key": api_key,
        }

        image_paths = glob.glob("mathml-images/images_filtered/*.png")
        self.json = json.dumps(
            {
                "urls": {
                    image: os.path.join(
                        "https://github.com/imzoc/mathpix-annotation/tree/master/mathml-images/images_filtered",
                        image,
                    )
                    for image in image_paths
                },
                ### IDRK what these do??
                # "math_inline_delimiters": ["$", "$"],
                # "rm_spaces": True,
                "formats": ["data", "html", "text"],
                "data_options": {
                    "include_mathml": True,
                    "include_latex": True,
                },
            }
        )

    def _get_date_str(self):
        return time.strftime(f"%m-%d-%Y", time.gmtime())

    def _gen_results_filename(self):
        batch_number = 0
        for file in glob.glob("results/*.json"):
            if file.startswith("results/raw-" + self._get_date()):
                local_batch_number = int(
                    file.split("-")[-1].replace(".json", "")
                )
                if local_batch_number >= batch_number:
                    batch_number = local_batch_number + 1

        return f"results/raw-{self._get_date()}-batch-{str(batch_number)}.json"

    def post_request(self):
        print("Sending POST request...")
        request = requests.post(
            self.url,
            json=self.json,
            headers=self.headers,
            timeout=30,
        )
        return request.json()

    def get_request(self, batch_id):
        print("Sending GET request...")
        request = requests.get(
            os.path.join(self.url, str(batch_id)),
            headers=self.headers,
        )
        return request.json()


class BatchResult:
    """This class handles"""

    def __init__(self, request_json):
        """
        self.original_file = image_file_name
        self.mathml = request["data"][0]["value"]
        self.latex = request["data"][1]["value"]
        self.mathpixml = request["text"]
        """
        pass

    def json(self):
        json_ = {
            "original_file": self.original_file,
            "mathml": self.mathml,
            "latex": self.latex,
            "mathpixml": self.mathpixml,
        }
        return json_
