class Logger:

    @staticmethod
    def log_request(request_type, url, params, response_status_code):
        print('Executed {} request.\nURL: {}\nPARAMETERS: {}\nResponse code: {}'.format(request_type, url, params, response_status_code))

    @staticmethod
    def log_response(response):
        print(response)

    @staticmethod
    def log_exception(message):
        print(message)
