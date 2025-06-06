from main import extract_title
import unittest

class Test_extract_title(unittest.TestCase):
	def test_normal_case(self):
		result = extract_title("# Title")
		expectation = "Title"
		print("CACAPROUT")
		self.assertEqual(result, expectation)

if __name__ == "__main__":
	unittest.main()	