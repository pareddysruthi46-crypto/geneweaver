import unittest

from gpu.prototype import run_array_prototype


class TestGPUPrototype(unittest.TestCase):

    def test_cpu_fallback_calculates_squares(self):
        result = run_array_prototype([1, 2, 3, 4, 5])
        self.assertEqual(result["result"], [1, 4, 9, 16, 25])

    def test_result_contains_execution_device(self):
        result = run_array_prototype([2, 3])
        self.assertIn(result["device"], ["CPU", "GPU"])

    def test_empty_array(self):
        result = run_array_prototype([])
        self.assertEqual(result["result"], [])

    def test_negative_values(self):
        result = run_array_prototype([-2, -3])
        self.assertEqual(result["result"], [4, 9])


if __name__ == "__main__":
    unittest.main()
