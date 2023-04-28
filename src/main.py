"""
This program sends requests to the Mathpix server.
"""

import glob
import json
import os
import sys
import time

import requests

### API KEY AUTHORIZATION
api_path = "internal/zach/api-key.txt"
with open(api_path) as api_key_file:
    API_KEY = str(api_key_file.readline())

### CONSTANTS
URL = "https://api.mathpix.com/v3/text"
HEADERS = {
    "app_id": "Zach's MathML requests",
    "app_key": API_KEY,
}
DATE = time.strftime(f"%m-%d-%Y", time.gmtime())

### IMAGES
IMG_DIR = "mathml-images/images_filtered"
IMAGES = glob.glob(os.path.join(IMG_DIR, "*.png"))


def main():
    results = take_3_images()
    write_results_to_file_raw(results)


def take_3_images():
    """Sends 3 POST requests via send_post_request."""
    return [send_post_request(image) for image in IMAGES[0:4]]


def send_post_request(image):
    """This function sends a post request with the image passed to it.
    It uses constants declared at the beginning of the script.
    """
    print("Sending POST request...")
    files = {"file": open(image, "rb")}
    options_json = json.dumps(
        {
            "math_inline_delimiters": ["$", "$"],
            "rm_spaces": True,
            "formats": ["text"],
        }
    )

    r = requests.post(
        URL,
        files=files,
        data={"options_json": options_json},
        headers=HEADERS,
    )
    result = json.dumps(r.json(), indent=4, sort_keys=True)
    return result


def write_results_to_file_raw(results):
    """This function writes results to a file in the results/
    directory.
    """
    batch_number = 0
    for file in glob.glob("results/*.json"):
        if file.startswith("results/raw-" + DATE):
            local_batch_number = int(
                file.split("-")[-1].replace(".json", "")
            )
            if local_batch_number >= batch_number:
                batch_number = local_batch_number + 1

    results_file_name = (
        f"results/raw-{DATE}-batch-{str(batch_number)}.json"
    )
    with open(results_file_name, "w") as file:
        for result in results:
            file.write(result)


if __name__ == "__main__":
    main()
