import handler


def main():
    request_handler = handler.RequestHandler()
    results_list = request_handler.take_n_images(3)
    request_handler.write_results_to_file(data)


main()
