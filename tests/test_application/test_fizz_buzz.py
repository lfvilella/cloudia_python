from application import services


class FakeService(services.ServiceBot):
    def _bot_reply(self, bot_reply_message, message_data):
        pass

    def _get_user_message(self, message_data) -> str:
        pass

    def _get_user_identifier(self, message_data) -> str:
        pass

    def _get_source_website(self) -> str:
        pass


class TestFizzBuzz:
    def test_with_wrong_number(self):
        assert (
            FakeService().get_fizz_buzz_message(1)
            == "Number 1 is not fizzbuzz..."
        )

    def test_with_fizz_number(self):
        assert FakeService().get_fizz_buzz_message(3) == "Fizz"

    def test_with_buzz_number(self):
        assert FakeService().get_fizz_buzz_message(5) == "Buzz"

    def test_with_fizz_buzz_number(self):
        assert FakeService().get_fizz_buzz_message(15) == "FizzBuzz"
