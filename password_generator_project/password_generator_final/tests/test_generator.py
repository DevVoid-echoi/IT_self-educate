import unittest
from src.generator import generate_password, evaluate_strength

class TestPasswordGenerator(unittest.TestCase):

    def test_password_length(self):
        length = 16
        pwd, _ = generate_password(length, True, True)
        self.assertEqual(len(pwd), length)

    def test_include_digits(self):
        pwd, _ = generate_password(10, include_nums=True, include_syms=False)
        self.assertTrue(any(c.isdigit() for c in pwd))

    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            generate_password(0, True, True)

if __name__ == "__main__":
    unittest.main()