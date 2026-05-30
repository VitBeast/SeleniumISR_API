
from adder.adder import Calculator


class TestCalc:
    def setup_method(self):
        self.calc = Calculator()

    def test_multiply_calculate_correctly(self):
        assert self.calc.multiply(2, 2) == 4

    def test_division_calculate_correctly(self):
        assert self.calc.division(6, 3) == 2

    def test_subtraction_calculate_correctly(self):
        assert self.calc.subtraction(5, 2) == 3

    def test_adding_calculate_correctly(self):
        assert self.calc.adding(3, 2) == 5

    def test_multiply_calculate_not_correctly(self):
        assert self.calc.multiply(3, 2) == 5

    def test_division_calculate_not_correctly(self):
        assert self.calc.division(6, 3) == 3

    def test_subtraction_calculate_not_correctly(self):
        assert self.calc.subtraction(6, 2) == 3

    def test_adding_calculate_not_correctly(self):
        assert self.calc.adding(6, 2) == 5