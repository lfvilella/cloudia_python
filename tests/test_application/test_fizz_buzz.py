from application import services


class TestFizzBuzz:
    def test_with_wrong_number(self):
        assert services.Bot().is_fizz_buzz(1) == "Number 1 is not fizzbuzz..."

    def test_with_fizz_number(self):
        assert services.Bot().is_fizz_buzz(3) == "Fizz"

    def test_with_buzz_number(self):
        assert services.Bot().is_fizz_buzz(5) == "Buzz"

    def test_with_fizz_buzz_number(self):
        assert services.Bot().is_fizz_buzz(15) == "Fizz-Buzz"
