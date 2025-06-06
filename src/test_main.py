from main import extract_title
import unittest

class Test_extract_title(unittest.TestCase):
	def test_normal_case(self):
		result = extract_title("# Title")
		expectation = "Title"
		self.assertEqual(result, expectation)

	def test_leading_space(self):
		with self.assertRaises(Exception):
			extract_title(" # Title")
			
	def test_stripped(self):
		result = extract_title("#  Title  ")
		expectation = "Title"
		self.assertEqual(result, expectation)

if __name__ == "__main__":
	unittest.main()	