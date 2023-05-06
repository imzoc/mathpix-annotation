class SingleRequestHandler:
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

    def take_n_images(self, n):
        """Sends n POST requests via send_post_request."""
        results_list = ResultsList()
        error_count = 0
        for image in self.images[0 : n + 1]:
            try:
                result = self.send_post_request(image)
                results_list.add(result)
            except:
                print("Encountered an error sending POST request.")
                print("Writing data to file and exiting...")
                break

        return results_list

    def take_all_images(self):
        """Sends POST requests for all images via take_n_images."""
        n = len(self.images)
        result = self.take_n_images(n - 1)
        return result

    def send_post_request(self, image):
        """This function sends a post request with the image passed to
        it. It generates a ResultsList object
        """
        print("Sending POST request...")

        req = requests.post(
            self.url,
            files={"file": open(image, "rb")},
            data={"options_json": options_json},
            headers=self.headers,
        )
        result = Result(req.json(), str(image))
        return result

    def write_results_to_file(self, results_list):
        """This function writes results from a results list
        to a file in the results/
        directory.
        """
        results_file_name = self._gen_results_file_name()
        json_ = {"results": []}
        for result in results_list.get_results_list():
            try:
                result_json = result.json()
            except:
                result_json = (
                    "Issue generating json from Result object..."
                )
            json_["results"].append(result_json)
        json_ = json.dumps(
            json_,
            indent=2,
        )
        with open(results_file_name, "w") as file:
            file.write(json_)

    def read_results_from_file(self, results_file):
        with open(results_file) as open_file:
            data = json.loads(open_file)

    def render_mathml(
        self,
    ):
        pass
