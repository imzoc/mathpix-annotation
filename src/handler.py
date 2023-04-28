"""
This program sends requests to the Mathpix server.
"""

import glob
import json
import os
import sys
import time

import requests


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

    def _get_date(self):
        return time.strftime(f"%m-%d-%Y", time.gmtime())

    def _gen_results_file_name(self):
        batch_number = 0
        for file in glob.glob("results/*.json"):
            if file.startswith("results/raw-" + self._get_date()):
                local_batch_number = int(
                    file.split("-")[-1].replace(".json", "")
                )
                if local_batch_number >= batch_number:
                    batch_number = local_batch_number + 1

        return f"results/raw-{self._get_date()}-batch-{str(batch_number)}.json"

    def take_n_images(self, n, allowed_errors=0):
        """Sends n POST requests via send_post_request."""
        results_list = ResultsList()
        error_count = 0
        for image in self.images[0 : n + 1]:
            # try:
            result = self.send_post_request(image)
            results_list.add(result)
            """
            except:
                print(
                    "Encountered an error sending POST request (line 37)."
                )
                error_count += 1
                print(f"Error count: {error_count}")
                if error_count == allowed_errors + 1:
                    print("Writing data to file and exiting...")
                    break
            """
        return results_list

    def send_post_request(self, image):
        """This function sends a post request with the image passed to
        it. It generates a ResultsList object
        """
        print("Sending POST request...")

        options_json = json.dumps(
            {
                "math_inline_delimiters": ["$", "$"],
                "rm_spaces": True,
                "formats": ["data", "html", "text"],
                "data_options": {
                    "include_mathml": True,
                    "include_latex": True,
                },
            }
        )

        req = requests.post(
            self.url,
            files={"file": open(image, "rb")},
            data={"options_json": options_json},
            headers=self.headers,
        )
        result = Result(req.json(), str(image))
        return result

    def write_results_to_file(self, results):
        """This function writes results from a results list
        to a file in the results/
        directory.
        """
        results_file_name = self._gen_results_file_name()
        with open(results_file_name, "w") as file:
            pass

    def read_results_from_file(self, results_file):
        with open(results_file) as open_file:
            data = json.loads(open_file)

    def render_mathml(
        self,
    ):
        pass


class Result:
    def __init__(self, request, image_file_name):
        self.original_file = image_file_name
        self.mathml = request["data"][0]["value"]
        self.latex = request["data"][1]["value"]
        self.mathpixml = request["text"]


class ResultsList:
    def __init__(self):
        self.results_list = []

    def add(self, result):
        self.results_list.append(result)

    def __repr__(self):
        return self.results_list
