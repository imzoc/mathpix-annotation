"""
This program generates json-formatted data about images
using MathPix's OCR API. It does so in stages so that data is not lost

"""


import handler


def main():
    request_handler = handler.RequestHandler()
    results_list = request_handler.take_all_images()
    request_handler.write_results_to_file(results_list)


main()
