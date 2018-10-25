from selenium import webdriver
import unittest

# browser = webdriver.Firefox(keep_alive=False)
# browser.get('http://localhost:8000')

# assert 'To-Do' in browser.title

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox(keep_alive=False)

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get('http://localhost:8000')

		self.assertIn('To-Do', self.browser.title)
		self.fail('Finish the test!')

		# Enter a to-do item

		# Type "buy chicken" into text box

		# When hitting enter, the page updates. Now the page lists "1. Buy chicken"

		# There is still a text box for input. Type "buy pb"

		# Page updates again, now showing both items on the list

		# Unique url is generated so that this list is remembered


# Only runs unittest when this .py program is run from terminal
if __name__ == '__main__':
	unittest.main(warnings='ignore')