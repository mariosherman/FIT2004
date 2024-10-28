import unittest
from q1 import fuse

def main():
    assert fuse([[0.0, 32, 0.7], [0.7, 20, 0.7], [0.7, 19, 0.2], [0.2, 17, 0.1], [0.1, 20, 0.9], [0.9, 80, 0.3], [0.3, 74, 0.2], [0.2, 52, 0.5], [0.5, 14, 0.2], [0.2, 89, 0.1], [0.1, 30, 0.8], [0.8, 60, 0.5], [0.5, 60, 0.6], [0.6, 73, 0.8], [0.8, 75, 0.6], [0.6, 72, 0.8], [0.8, 61, 0.2], [0.2, 98, 0.5], [0.5, 52, 0.6], [0.6, 15, 0.9], [0.9, 26, 0.4], [0.4, 83, 0.7], [0.7, 32, 0.4], [0.4, 46, 0.7], [0.7, 27, 0.9], [0.9, 46, 0.3], [0.3, 79, 0.5], [0.5, 27, 0.6], [0.6, 85, 0.6], [0.6, 29, 0.2], [0.2, 46, 0.1], [0.1, 12, 0.8], [0.8, 65, 0.4], [0.4, 90, 0.7], [0.7, 96, 0.8], [0.8, 42, 0.5], [0.5, 35, 0.6], [0.6, 15, 0.2], [0.2, 52, 0.7], [0.7, 65, 0.6], [0.6, 42, 0.8], [0.8, 31, 0.3], [0.3, 41, 0.2], [0.2, 46, 0.4], [0.4, 16, 0.7], [0.7, 11, 0.7], [0.7, 22, 0.5], [0.5, 42, 0.8], [0.8, 55, 0.2], [0.2, 66, 0.4], [0.4, 97, 0.1], [0.1, 59, 0.2], [0.2, 65, 0.8], [0.8, 13, 0.3], [0.3, 31, 0.7], [0.7, 18, 0.7], [0.7, 89, 0.1], [0.1, 18, 0.5], [0.5, 24, 0.8], [0.8, 99, 0.8], [0.8, 35, 0.6], [0.6, 43, 0.8], [0.8, 74, 0.6], [0.6, 49, 0.1], [0.1, 61, 0.6], [0.6, 96, 0.9], [0.9, 35, 0.2], [0.2, 91, 0.3], [0.3, 87, 0.3], [0.3, 77, 0.2], [0.2, 89, 0.8], [0.8, 48, 0.8], [0.8, 49, 0.2], [0.2, 50, 0.2], [0.2, 58, 0.6], [0.6, 48, 0.4], [0.4, 17, 0.6], [0.6, 48, 0.5], [0.5, 89, 0.7], [0.7, 22, 0.4], [0.4, 68, 0.4], [0.4, 18, 0.3], [0.3, 40, 0.7], [0.7, 89, 0.8], [0.8, 52, 0.8], [0.8, 80, 0.7], [0.7, 76, 0.2], [0.2, 66, 0.6], [0.6, 25, 0.3], [0.3, 51, 0.3], [0.3, 73, 0.9], [0.9, 53, 0.5], [0.5, 77, 0.7], [0.7, 40, 0.7], [0.7, 81, 0.8], [0.8, 37, 0.9], [0.9, 66, 0.8], [0.8, 98, 0.5], [0.5, 27, 0.8], [0.8, 14, 0.3], [0.3, 94, 0.3], [0.3, 19, 0.2], [0.2, 10, 0.3], [0.3, 53, 0.2], [0.2, 84, 0.5], [0.5, 37, 0.2], [0.2, 57, 0.5], [0.5, 80, 0.2], [0.2, 78, 0.6], [0.6, 53, 0.7], [0.7, 16, 0.6], [0.6, 12, 0.7], [0.7, 94, 0.5], [0.5, 91, 0.4], [0.4, 10, 0.9], [0.9, 71, 0.6], [0.6, 67, 0.2], [0.2, 51, 0.7], [0.7, 92, 0.6], [0.6, 38, 0.6], [0.6, 94, 0.4], [0.4, 26, 0.4], [0.4, 25, 0.2], [0.2, 27, 0.6], [0.6, 92, 0.4], [0.4, 22, 0.3], [0.3, 77, 0.5], [0.5, 47, 0.5], [0.5, 39, 0.8], [0.8, 94, 0.2], [0.2, 50, 0.4], [0.4, 95, 0.3], [0.3, 58, 0.6], [0.6, 24, 0.7], [0.7, 52, 0.3], [0.3, 62, 0.5], [0.5, 64, 0.4], [0.4, 30, 0.3], [0.3, 26, 0.5], [0.5, 65, 0.4], [0.4, 37, 0.1], [0.1, 41, 0.6], [0.6, 77, 0.4], [0.4, 43, 0.5], [0.5, 96, 0.1], [0.1, 53, 0.3], [0.3, 80, 0.7], [0.7, 14, 0.8], [0.8, 79, 0.8], [0.8, 89, 0.2], [0.2, 67, 0.2], [0.2, 55, 0.7], [0.7, 88, 0.3], [0.3, 85, 0.4], [0.4, 28, 0.5], [0.5, 33, 0.5], [0.5, 83, 0.4], [0.4, 27, 0.6], [0.6, 33, 0.6], [0.6, 91, 0.6], [0.6, 67, 0.3], [0.3, 12, 0.4], [0.4, 61, 0.7], [0.7, 49, 0.8], [0.8, 13, 0.1], [0.1, 93, 0.9], [0.9, 86, 0.3], [0.3, 70, 0.3], [0.3, 41, 0.2], [0.2, 74, 0.6], [0.6, 91, 0.8], [0.8, 91, 0.7], [0.7, 17, 0.5], [0.5, 33, 0.1], [0.1, 12, 0.8], [0.8, 30, 0.1], [0.1, 25, 0.6], [0.6, 88, 0.8], [0.8, 83, 0.3], [0.3, 81, 0.2], [0.2, 82, 0.3], [0.3, 34, 0.7], [0.7, 36, 0.6], [0.6, 18, 0.8], [0.8, 62, 0.8], [0.8, 19, 0.6], [0.6, 94, 0.1], [0.1, 23, 0.3], [0.3, 88, 0.3], [0.3, 82, 0.8], [0.8, 19, 0.3], [0.3, 51, 0.4], [0.4, 87, 0.9], [0.9, 30, 0.3], [0.3, 70, 0.1], [0.1, 75, 0.5], [0.5, 77, 0.5], [0.5, 77, 0.8], [0.8, 11, 0.6], [0.6, 86, 0.1], [0.1, 76, 0.8], [0.8, 38, 0.5], [0.5, 59, 0.8], [0.8, 37, 0.8], [0.8, 52, 0.4], [0.4, 70, 0.7], [0.7, 15, 0.5], [0.5, 83, 0.5], [0.5, 27, 0.5], [0.5, 45, 0.7], [0.7, 23, 0.5], [0.5, 93, 0.5], [0.5, 25, 0.7], [0.7, 27, 0.9], [0.9, 78, 0.8], [0.8, 38, 0.4], [0.4, 29, 0.6], [0.6, 49, 0.2], [0.2, 27, 0.6], [0.6, 75, 0.4], [0.4, 63, 0.8], [0.8, 42, 0.1], [0.1, 64, 0.7], [0.7, 28, 0.1], [0.1, 96, 0.1], [0.1, 100, 0.6], [0.6, 57, 0.8], [0.8, 95, 0.3], [0.3, 31, 0.2], [0.2, 89, 0.4], [0.4, 70, 0.4], [0.4, 19, 0.8], [0.8, 82, 0.3], [0.3, 84, 0.7], [0.7, 44, 0.5], [0.5, 98, 0.7], [0.7, 62, 0.2], [0.2, 100, 0.7], [0.7, 52, 0.1], [0.1, 32, 0.4], [0.4, 87, 0.9], [0.9, 24, 0.1], [0.1, 95, 0.4], [0.4, 66, 0.6], [0.6, 81, 0.2], [0.2, 96, 0.3], [0.3, 80, 0.7], [0.7, 83, 0.4], [0.4, 77, 0.6], [0.6, 47, 0.2], [0.2, 89, 0.6], [0.6, 37, 0.4], [0.4, 16, 0.8], [0.8, 38, 0.8], [0.8, 15, 0.7], [0.7, 17, 0.5], [0.5, 74, 0.5], [0.5, 41, 0.2], [0.2, 34, 0.2], [0.2, 13, 0.3], [0.3, 34, 0.5], [0.5, 45, 0.7], [0.7, 35, 0.3], [0.3, 18, 0.7], [0.7, 95, 0.2], [0.2, 40, 0.6], [0.6, 90, 0.2], [0.2, 42, 0.3], [0.3, 63, 0.1], [0.1, 56, 0.3], [0.3, 64, 0.4], [0.4, 96, 0.9], [0.9, 29, 0.8], [0.8, 85, 0.4], [0.4, 72, 0.3], [0.3, 59, 0.6], [0.6, 53, 0.4], [0.4, 76, 0.5], [0.5, 45, 0.6], [0.6, 87, 0.3], [0.3, 14, 0.8], [0.8, 88, 0.9], [0.9, 90, 0.6], [0.6, 18, 0.5], [0.5, 71, 0.9], [0.9, 33, 0.8], [0.8, 28, 0.2], [0.2, 73, 0.3], [0.3, 31, 0.2], [0.2, 67, 0.5], [0.5, 46, 0.8], [0.8, 72, 0.8], [0.8, 51, 0.6], [0.6, 80, 0.4], [0.4, 57, 0.8], [0.8, 96, 0.3], [0.3, 31, 0.2], [0.2, 80, 0.5], [0.5, 66, 0.2], [0.2, 10, 0.7], [0.7, 10, 0.9], [0.9, 39, 0.3], [0.3, 25, 0.4], [0.4, 55, 0.3], [0.3, 43, 0.4], [0.4, 49, 0.2], [0.2, 26, 0.3], [0.3, 18, 0.7], [0.7, 79, 0.6], [0.6, 79, 0.4], [0.4, 94, 0.3], [0.3, 51, 0.4], [0.4, 40, 0.3], [0.3, 45, 0.3], [0.3, 81, 0.3], [0.3, 77, 0.3], [0.3, 67, 0.6], [0.6, 38, 0.8], [0.8, 87, 0.9], [0.9, 46, 0.7], [0.7, 47, 0.2], [0.2, 40, 0.4], [0.4, 45, 0.3], [0.3, 49, 0.1], [0.1, 66, 0.4], [0.4, 40, 0.3], [0.3, 72, 0.3], [0.3, 67, 0.2], [0.2, 92, 0.5], [0.5, 11, 0.8], [0.8, 80, 0.2], [0.2, 55, 0.4], [0.4, 58, 0.3], [0.3, 25, 0.7], [0.7, 34, 0.3], [0.3, 78, 0.2], [0.2, 94, 0.2], [0.2, 22, 0.9], [0.9, 30, 0.2], [0.2, 44, 0.8], [0.8, 10, 0.3], [0.3, 24, 0.1], [0.1, 43, 0.9], [0.9, 34, 0.8], [0.8, 97, 0.2], [0.2, 85, 0.1], [0.1, 86, 0.8], [0.8, 66, 0.3], [0.3, 71, 0.5], [0.5, 69, 0.3], [0.3, 54, 0.3], [0.3, 13, 0.7], [0.7, 29, 0.6], [0.6, 80, 0.2], [0.2, 82, 0.7], [0.7, 94, 0.5], [0.5, 74, 0.3], [0.3, 20, 0.2], [0.2, 86, 0.1], [0.1, 42, 0.9], [0.9, 90, 0.8], [0.8, 35, 0.8], [0.8, 31, 0.5], [0.5, 13, 0.5], [0.5, 33, 0.5], [0.5, 30, 0.6], [0.6, 26, 0.5], [0.5, 15, 0.8], [0.8, 96, 0.7], [0.7, 88, 0.8], [0.8, 74, 0.8], [0.8, 50, 0.7], [0.7, 40, 0.6], [0.6, 99, 0.5], [0.5, 57, 0.4], [0.4, 18, 0.4], [0.4, 82, 0.5], [0.5, 42, 0.3], [0.3, 50, 0.7], [0.7, 51, 0.3], [0.3, 57, 0.3], [0.3, 16, 0.2], [0.2, 44, 0.9], [0.9, 32, 0.3], [0.3, 63, 0.2], [0.2, 66, 0.2], [0.2, 14, 0.5], [0.5, 27, 0.3], [0.3, 81, 0.4], [0.4, 92, 0.9], [0.9, 60, 0.6], [0.6, 90, 0.8], [0.8, 15, 0.5], [0.5, 65, 0.7], [0.7, 56, 0.8], [0.8, 69, 0.3], [0.3, 10, 0.7], [0.7, 81, 0.7], [0.7, 30, 0.9], [0.9, 50, 0.8], [0.8, 91, 0.2], [0.2, 24, 0.8], [0.8, 89, 0.5], [0.5, 81, 0.9], [0.9, 87, 0.3], [0.3, 54, 0.8], [0.8, 68, 0.2], [0.2, 94, 0.4], [0.4, 48, 0.3], [0.3, 97, 0.5], [0.5, 52, 0.7], [0.7, 73, 0.5], [0.5, 75, 0.9], [0.9, 97, 0.1], [0.1, 86, 0.6], [0.6, 50, 0.2], [0.2, 53, 0.6], [0.6, 21, 0.9], [0.9, 24, 0.3], [0.3, 15, 0.6], [0.6, 83, 0.9], [0.9, 11, 0.4], [0.4, 68, 0.4], [0.4, 38, 0.9], [0.9, 62, 0.5], [0.5, 58, 0.8], [0.8, 44, 0.7], [0.7, 92, 0.5], [0.5, 93, 0.4], [0.4, 10, 0.8], [0.8, 63, 0.7], [0.7, 27, 0.6], [0.6, 79, 0.2], [0.2, 65, 0.6], [0.6, 100, 0.4], [0.4, 74, 0.6], [0.6, 50, 0.1], [0.1, 38, 0.1], [0.1, 50, 0.1], [0.1, 71, 0.4], [0.4, 64, 0.6], [0.6, 26, 0.6], [0.6, 29, 0.5], [0.5, 28, 0.5], [0.5, 40, 0.7], [0.7, 55, 0.2], [0.2, 18, 0.8], [0.8, 84, 0.2], [0.2, 94, 0.5], [0.5, 91, 0.4], [0.4, 77, 0.1], [0.1, 15, 0.3], [0.3, 85, 0.1], [0.1, 100, 0.4], [0.4, 89, 0.3], [0.3, 46, 0.3], [0.3, 16, 0.3], [0.3, 64, 0.1], [0.1, 68, 0.6], [0.6, 45, 0.8], [0.8, 40, 0.5], [0.5, 11, 0.3], [0.3, 32, 0.8], [0.8, 63, 0.8], [0.8, 57, 0.8], [0.8, 26, 0.4], [0.4, 71, 0.8], [0.8, 24, 0.9], [0.9, 84, 0.3], [0.3, 84, 0.4], [0.4, 50, 0.3], [0.3, 81, 0.7], [0.7, 12, 0.8], [0.8, 82, 0.3], [0.3, 90, 0.2], [0.2, 57, 0.5], [0.5, 32, 0.7], [0.7, 21, 0.5], [0.5, 89, 0.5], [0.5, 59, 0.8], [0.8, 33, 0.7], [0.7, 33, 0.2], [0.2, 94, 0.4], [0.4, 23, 0.3], [0.3, 90, 0.8], [0.8, 92, 0.1], [0.1, 89, 0.7], [0.7, 21, 0.7], [0.7, 92, 0.7], [0.7, 21, 0.7], [0.7, 90, 0.6], [0.6, 47, 0.7], [0.7, 31, 0.5], [0.5, 70, 0.2], [0.2, 21, 0.2], [0.2, 55, 0.2], [0.2, 62, 0.5], [0.5, 25, 0.2], [0.2, 58, 0.5], [0.5, 45, 0.0]]) == 2218
    
class TestProblem3(unittest.TestCase):
    """
    This contains all staff provided testcases and the faster student provided ones.
    """
    def test_example_1(self):
        got = fuse([[0.0, 32, 0.7], [0.7, 20, 0.7], [0.7, 19, 0.2], [0.2, 17, 0.1], [0.1, 20, 0.9], [0.9, 80, 0.3], [0.3, 74, 0.2], [0.2, 52, 0.5], [0.5, 14, 0.2], [0.2, 89, 0.1], [0.1, 30, 0.8], [0.8, 60, 0.5], [0.5, 60, 0.6], [0.6, 73, 0.8], [0.8, 75, 0.6], [0.6, 72, 0.8], [0.8, 61, 0.2], [0.2, 98, 0.5], [0.5, 52, 0.6], [0.6, 15, 0.9], [0.9, 26, 0.4], [0.4, 83, 0.7], [0.7, 32, 0.4], [0.4, 46, 0.7], [0.7, 27, 0.9], [0.9, 46, 0.3], [0.3, 79, 0.5], [0.5, 27, 0.6], [0.6, 85, 0.6], [0.6, 29, 0.2], [0.2, 46, 0.1], [0.1, 12, 0.8], [0.8, 65, 0.4], [0.4, 90, 0.7], [0.7, 96, 0.8], [0.8, 42, 0.5], [0.5, 35, 0.6], [0.6, 15, 0.2], [0.2, 52, 0.7], [0.7, 65, 0.6], [0.6, 42, 0.8], [0.8, 31, 0.3], [0.3, 41, 0.2], [0.2, 46, 0.4], [0.4, 16, 0.7], [0.7, 11, 0.7], [0.7, 22, 0.5], [0.5, 42, 0.8], [0.8, 55, 0.2], [0.2, 66, 0.4], [0.4, 97, 0.1], [0.1, 59, 0.2], [0.2, 65, 0.8], [0.8, 13, 0.3], [0.3, 31, 0.7], [0.7, 18, 0.7], [0.7, 89, 0.1], [0.1, 18, 0.5], [0.5, 24, 0.8], [0.8, 99, 0.8], [0.8, 35, 0.6], [0.6, 43, 0.8], [0.8, 74, 0.6], [0.6, 49, 0.1], [0.1, 61, 0.6], [0.6, 96, 0.9], [0.9, 35, 0.2], [0.2, 91, 0.3], [0.3, 87, 0.3], [0.3, 77, 0.2], [0.2, 89, 0.8], [0.8, 48, 0.8], [0.8, 49, 0.2], [0.2, 50, 0.2], [0.2, 58, 0.6], [0.6, 48, 0.4], [0.4, 17, 0.6], [0.6, 48, 0.5], [0.5, 89, 0.7], [0.7, 22, 0.4], [0.4, 68, 0.4], [0.4, 18, 0.3], [0.3, 40, 0.7], [0.7, 89, 0.8], [0.8, 52, 0.8], [0.8, 80, 0.7], [0.7, 76, 0.2], [0.2, 66, 0.6], [0.6, 25, 0.3], [0.3, 51, 0.3], [0.3, 73, 0.9], [0.9, 53, 0.5], [0.5, 77, 0.7], [0.7, 40, 0.7], [0.7, 81, 0.8], [0.8, 37, 0.9], [0.9, 66, 0.8], [0.8, 98, 0.5], [0.5, 27, 0.8], [0.8, 14, 0.3], [0.3, 94, 0.3], [0.3, 19, 0.2], [0.2, 10, 0.3], [0.3, 53, 0.2], [0.2, 84, 0.5], [0.5, 37, 0.2], [0.2, 57, 0.5], [0.5, 80, 0.2], [0.2, 78, 0.6], [0.6, 53, 0.7], [0.7, 16, 0.6], [0.6, 12, 0.7], [0.7, 94, 0.5], [0.5, 91, 0.4], [0.4, 10, 0.9], [0.9, 71, 0.6], [0.6, 67, 0.2], [0.2, 51, 0.7], [0.7, 92, 0.6], [0.6, 38, 0.6], [0.6, 94, 0.4], [0.4, 26, 0.4], [0.4, 25, 0.2], [0.2, 27, 0.6], [0.6, 92, 0.4], [0.4, 22, 0.3], [0.3, 77, 0.5], [0.5, 47, 0.5], [0.5, 39, 0.8], [0.8, 94, 0.2], [0.2, 50, 0.4], [0.4, 95, 0.3], [0.3, 58, 0.6], [0.6, 24, 0.7], [0.7, 52, 0.3], [0.3, 62, 0.5], [0.5, 64, 0.4], [0.4, 30, 0.3], [0.3, 26, 0.5], [0.5, 65, 0.4], [0.4, 37, 0.1], [0.1, 41, 0.6], [0.6, 77, 0.4], [0.4, 43, 0.5], [0.5, 96, 0.1], [0.1, 53, 0.3], [0.3, 80, 0.7], [0.7, 14, 0.8], [0.8, 79, 0.8], [0.8, 89, 0.2], [0.2, 67, 0.2], [0.2, 55, 0.7], [0.7, 88, 0.3], [0.3, 85, 0.4], [0.4, 28, 0.5], [0.5, 33, 0.5], [0.5, 83, 0.4], [0.4, 27, 0.6], [0.6, 33, 0.6], [0.6, 91, 0.6], [0.6, 67, 0.3], [0.3, 12, 0.4], [0.4, 61, 0.7], [0.7, 49, 0.8], [0.8, 13, 0.1], [0.1, 93, 0.9], [0.9, 86, 0.3], [0.3, 70, 0.3], [0.3, 41, 0.2], [0.2, 74, 0.6], [0.6, 91, 0.8], [0.8, 91, 0.7], [0.7, 17, 0.5], [0.5, 33, 0.1], [0.1, 12, 0.8], [0.8, 30, 0.1], [0.1, 25, 0.6], [0.6, 88, 0.8], [0.8, 83, 0.3], [0.3, 81, 0.2], [0.2, 82, 0.3], [0.3, 34, 0.7], [0.7, 36, 0.6], [0.6, 18, 0.8], [0.8, 62, 0.8], [0.8, 19, 0.6], [0.6, 94, 0.1], [0.1, 23, 0.3], [0.3, 88, 0.3], [0.3, 82, 0.8], [0.8, 19, 0.3], [0.3, 51, 0.4], [0.4, 87, 0.9], [0.9, 30, 0.3], [0.3, 70, 0.1], [0.1, 75, 0.5], [0.5, 77, 0.5], [0.5, 77, 0.8], [0.8, 11, 0.6], [0.6, 86, 0.1], [0.1, 76, 0.8], [0.8, 38, 0.5], [0.5, 59, 0.8], [0.8, 37, 0.8], [0.8, 52, 0.4], [0.4, 70, 0.7], [0.7, 15, 0.5], [0.5, 83, 0.5], [0.5, 27, 0.5], [0.5, 45, 0.7], [0.7, 23, 0.5], [0.5, 93, 0.5], [0.5, 25, 0.7], [0.7, 27, 0.9], [0.9, 78, 0.8], [0.8, 38, 0.4], [0.4, 29, 0.6], [0.6, 49, 0.2], [0.2, 27, 0.6], [0.6, 75, 0.4], [0.4, 63, 0.8], [0.8, 42, 0.1], [0.1, 64, 0.7], [0.7, 28, 0.1], [0.1, 96, 0.1], [0.1, 100, 0.6], [0.6, 57, 0.8], [0.8, 95, 0.3], [0.3, 31, 0.2], [0.2, 89, 0.4], [0.4, 70, 0.4], [0.4, 19, 0.8], [0.8, 82, 0.3], [0.3, 84, 0.7], [0.7, 44, 0.5], [0.5, 98, 0.7], [0.7, 62, 0.2], [0.2, 100, 0.7], [0.7, 52, 0.1], [0.1, 32, 0.4], [0.4, 87, 0.9], [0.9, 24, 0.1], [0.1, 95, 0.4], [0.4, 66, 0.6], [0.6, 81, 0.2], [0.2, 96, 0.3], [0.3, 80, 0.7], [0.7, 83, 0.4], [0.4, 77, 0.6], [0.6, 47, 0.2], [0.2, 89, 0.6], [0.6, 37, 0.4], [0.4, 16, 0.8], [0.8, 38, 0.8], [0.8, 15, 0.7], [0.7, 17, 0.5], [0.5, 74, 0.5], [0.5, 41, 0.2], [0.2, 34, 0.2], [0.2, 13, 0.3], [0.3, 34, 0.5], [0.5, 45, 0.7], [0.7, 35, 0.3], [0.3, 18, 0.7], [0.7, 95, 0.2], [0.2, 40, 0.6], [0.6, 90, 0.2], [0.2, 42, 0.3], [0.3, 63, 0.1], [0.1, 56, 0.3], [0.3, 64, 0.4], [0.4, 96, 0.9], [0.9, 29, 0.8], [0.8, 85, 0.4], [0.4, 72, 0.3], [0.3, 59, 0.6], [0.6, 53, 0.4], [0.4, 76, 0.5], [0.5, 45, 0.6], [0.6, 87, 0.3], [0.3, 14, 0.8], [0.8, 88, 0.9], [0.9, 90, 0.6], [0.6, 18, 0.5], [0.5, 71, 0.9], [0.9, 33, 0.8], [0.8, 28, 0.2], [0.2, 73, 0.3], [0.3, 31, 0.2], [0.2, 67, 0.5], [0.5, 46, 0.8], [0.8, 72, 0.8], [0.8, 51, 0.6], [0.6, 80, 0.4], [0.4, 57, 0.8], [0.8, 96, 0.3], [0.3, 31, 0.2], [0.2, 80, 0.5], [0.5, 66, 0.2], [0.2, 10, 0.7], [0.7, 10, 0.9], [0.9, 39, 0.3], [0.3, 25, 0.4], [0.4, 55, 0.3], [0.3, 43, 0.4], [0.4, 49, 0.2], [0.2, 26, 0.3], [0.3, 18, 0.7], [0.7, 79, 0.6], [0.6, 79, 0.4], [0.4, 94, 0.3], [0.3, 51, 0.4], [0.4, 40, 0.3], [0.3, 45, 0.3], [0.3, 81, 0.3], [0.3, 77, 0.3], [0.3, 67, 0.6], [0.6, 38, 0.8], [0.8, 87, 0.9], [0.9, 46, 0.7], [0.7, 47, 0.2], [0.2, 40, 0.4], [0.4, 45, 0.3], [0.3, 49, 0.1], [0.1, 66, 0.4], [0.4, 40, 0.3], [0.3, 72, 0.3], [0.3, 67, 0.2], [0.2, 92, 0.5], [0.5, 11, 0.8], [0.8, 80, 0.2], [0.2, 55, 0.4], [0.4, 58, 0.3], [0.3, 25, 0.7], [0.7, 34, 0.3], [0.3, 78, 0.2], [0.2, 94, 0.2], [0.2, 22, 0.9], [0.9, 30, 0.2], [0.2, 44, 0.8], [0.8, 10, 0.3], [0.3, 24, 0.1], [0.1, 43, 0.9], [0.9, 34, 0.8], [0.8, 97, 0.2], [0.2, 85, 0.1], [0.1, 86, 0.8], [0.8, 66, 0.3], [0.3, 71, 0.5], [0.5, 69, 0.3], [0.3, 54, 0.3], [0.3, 13, 0.7], [0.7, 29, 0.6], [0.6, 80, 0.2], [0.2, 82, 0.7], [0.7, 94, 0.5], [0.5, 74, 0.3], [0.3, 20, 0.2], [0.2, 86, 0.1], [0.1, 42, 0.9], [0.9, 90, 0.8], [0.8, 35, 0.8], [0.8, 31, 0.5], [0.5, 13, 0.5], [0.5, 33, 0.5], [0.5, 30, 0.6], [0.6, 26, 0.5], [0.5, 15, 0.8], [0.8, 96, 0.7], [0.7, 88, 0.8], [0.8, 74, 0.8], [0.8, 50, 0.7], [0.7, 40, 0.6], [0.6, 99, 0.5], [0.5, 57, 0.4], [0.4, 18, 0.4], [0.4, 82, 0.5], [0.5, 42, 0.3], [0.3, 50, 0.7], [0.7, 51, 0.3], [0.3, 57, 0.3], [0.3, 16, 0.2], [0.2, 44, 0.9], [0.9, 32, 0.3], [0.3, 63, 0.2], [0.2, 66, 0.2], [0.2, 14, 0.5], [0.5, 27, 0.3], [0.3, 81, 0.4], [0.4, 92, 0.9], [0.9, 60, 0.6], [0.6, 90, 0.8], [0.8, 15, 0.5], [0.5, 65, 0.7], [0.7, 56, 0.8], [0.8, 69, 0.3], [0.3, 10, 0.7], [0.7, 81, 0.7], [0.7, 30, 0.9], [0.9, 50, 0.8], [0.8, 91, 0.2], [0.2, 24, 0.8], [0.8, 89, 0.5], [0.5, 81, 0.9], [0.9, 87, 0.3], [0.3, 54, 0.8], [0.8, 68, 0.2], [0.2, 94, 0.4], [0.4, 48, 0.3], [0.3, 97, 0.5], [0.5, 52, 0.7], [0.7, 73, 0.5], [0.5, 75, 0.9], [0.9, 97, 0.1], [0.1, 86, 0.6], [0.6, 50, 0.2], [0.2, 53, 0.6], [0.6, 21, 0.9], [0.9, 24, 0.3], [0.3, 15, 0.6], [0.6, 83, 0.9], [0.9, 11, 0.4], [0.4, 68, 0.4], [0.4, 38, 0.9], [0.9, 62, 0.5], [0.5, 58, 0.8], [0.8, 44, 0.7], [0.7, 92, 0.5], [0.5, 93, 0.4], [0.4, 10, 0.8], [0.8, 63, 0.7], [0.7, 27, 0.6], [0.6, 79, 0.2], [0.2, 65, 0.6], [0.6, 100, 0.4], [0.4, 74, 0.6], [0.6, 50, 0.1], [0.1, 38, 0.1], [0.1, 50, 0.1], [0.1, 71, 0.4], [0.4, 64, 0.6], [0.6, 26, 0.6], [0.6, 29, 0.5], [0.5, 28, 0.5], [0.5, 40, 0.7], [0.7, 55, 0.2], [0.2, 18, 0.8], [0.8, 84, 0.2], [0.2, 94, 0.5], [0.5, 91, 0.4], [0.4, 77, 0.1], [0.1, 15, 0.3], [0.3, 85, 0.1], [0.1, 100, 0.4], [0.4, 89, 0.3], [0.3, 46, 0.3], [0.3, 16, 0.3], [0.3, 64, 0.1], [0.1, 68, 0.6], [0.6, 45, 0.8], [0.8, 40, 0.5], [0.5, 11, 0.3], [0.3, 32, 0.8], [0.8, 63, 0.8], [0.8, 57, 0.8], [0.8, 26, 0.4], [0.4, 71, 0.8], [0.8, 24, 0.9], [0.9, 84, 0.3], [0.3, 84, 0.4], [0.4, 50, 0.3], [0.3, 81, 0.7], [0.7, 12, 0.8], [0.8, 82, 0.3], [0.3, 90, 0.2], [0.2, 57, 0.5], [0.5, 32, 0.7], [0.7, 21, 0.5], [0.5, 89, 0.5], [0.5, 59, 0.8], [0.8, 33, 0.7], [0.7, 33, 0.2], [0.2, 94, 0.4], [0.4, 23, 0.3], [0.3, 90, 0.8], [0.8, 92, 0.1], [0.1, 89, 0.7], [0.7, 21, 0.7], [0.7, 92, 0.7], [0.7, 21, 0.7], [0.7, 90, 0.6], [0.6, 47, 0.7], [0.7, 31, 0.5], [0.5, 70, 0.2], [0.2, 21, 0.2], [0.2, 55, 0.2], [0.2, 62, 0.5], [0.5, 25, 0.2], [0.2, 58, 0.5], [0.5, 45, 0.0]])
        expected = 2218
        self.assertEqual(expected, got, f"expected {expected}, got {got}")

if __name__ == '__main__':
    unittest.main()
    