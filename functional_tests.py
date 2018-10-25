from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
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
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# Enter a to-do item
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
			)

		# Type "buy chicken" into text box
		inputbox.send_keys('Buy chicken')

		# When hitting enter, the page updates. Now the page lists "1. Buy chicken"
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(any(row.text == '1: Buy chicken' for row in rows))

		# There is still a text box for input. Type "buy pb"
		self.fail('Finish the test!')

		# Page updates again, now showing both items on the list

		# Unique url is generated so that this list is remembered


# Only runs unittest when this .py program is run from terminal
if __name__ == '__main__':
	unittest.main(warnings='ignore')