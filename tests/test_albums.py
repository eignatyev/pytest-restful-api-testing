from asserter import assert_true, assert_equal
from session import Endpoints, HTTPSession, RequestTypes, StatusCodes
from test_utils import decorate_test, measure_time

ENDPOINT = Endpoints.ALBUMS

class TestAlbums:

    @staticmethod
    @decorate_test
    def test_status_code():
        status_code, _ = HTTPSession.send_request(RequestTypes.GET, ENDPOINT)
        assert_equal(status_code, StatusCodes.STATUS_200, f'Status code of {ENDPOINT} enpoint')

    @staticmethod
    @decorate_test
    def test_returned_list_length():
        _, data = HTTPSession.send_request(RequestTypes.GET, ENDPOINT)
        expected_list_size = 100
        assert_equal(len(data), expected_list_size, 'Amount of returned data entities')


    @staticmethod
    @decorate_test
    def test_data_structure():
        _, albums = HTTPSession.send_request(RequestTypes.GET, ENDPOINT)
        assert_equal(type(albums), list, 'The upper level data type')
        assert_true(all([isinstance(a, dict) for a in albums]), 'All album entities data type is dict')
        user_ids = [isinstance(a.get('userId', None), int) for a in albums]
        assert_true(all(user_ids), 'All album entities have "userId" attribute of int type')
        ids = [isinstance(a.get('id', None), int) for a in albums]
        assert_true(all(ids), 'All album entities have "id" attribute of int type')
        titles = [a.get('title', None) for a in albums]
        titles_data_type_checks = []
        titles_fullness_checks = []
        for t in titles:
            titles_data_type_checks.append(isinstance(t, str))
            titles_fullness_checks.append(bool(t))
        assert_true(all(titles_data_type_checks), 'All album entities have "title" attribute of str type')
        assert_true(all(titles_fullness_checks), 'All album entities have non-empty titles')

    @staticmethod
    @decorate_test
    def test_homogeneity_of_service_responses_time():
        num_of_iterations = 100
        allowed_time_delta = 0.15  # in seconds
        measured_time_list = []
        for _ in range(num_of_iterations):
            measured_time, (status_code, _) = measure_time(lambda: HTTPSession.send_request(RequestTypes.GET, ENDPOINT, do_logging=False))
            if str(status_code) != StatusCodes.STATUS_200:
                assert False, f'Service responded with status code: {status_code}'
            measured_time_list.append(measured_time)
        time_difference = max(measured_time_list) - min(measured_time_list)
        assert_true(
            time_difference <= allowed_time_delta,
            f'Difference ({time_difference}) in {ENDPOINT} response speed in not bigger than {allowed_time_delta}s'
        )
