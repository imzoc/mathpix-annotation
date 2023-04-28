import json

import handler


def main():
    request_handler = handler.RequestHandler()
    results_list = request_handler.take_n_images(3)
    for result in results_list:
        


main()
