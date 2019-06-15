from password_web import generator


class TestApiService():
    def test_bad_host(self):
        assert generator.call_password_service("bad_host:5000", 10, False, False, False)["error"]