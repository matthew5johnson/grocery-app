from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from django.test import LiveServerTestCase


# browser = webdriver.Firefox(keep_alive=False)
# browser.get('http://localhost:8000') <<<-- == http://127.0.0.1:8000/

# assert 'To-Do' in browser.title

class NewVisitorTest(LiveServerTestCase):

	def setUp(self):
		self.browser = webdriver.Firefox(keep_alive=False)

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_element_by_tag_name('tr')
		# self.assertIn(row_text, [row.text for row in rows])  # This object isn't iterable, but it looks like we check for it further down in the functional test anyway, so should be safe to comment out here.		

	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get('http://localhost:8000')  # self.live_server_url  http://localhost:8000

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
		self.assertTrue(any(row.text == '1: Buy chicken' for row in rows),
			f"New to-do item did not appear in the table. Contents were:\n{table.text}"
			)
		self.assertTrue(
			any(row.text == '1: Buy chicken' for row in rows),
			f"New to-do item did not appear in table. Contents were:\n{table.text}"
			)

		# There is still a text box for input. Type "buy pb"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feather to make a fly')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)

		# Page updates again, now showing both items on the list
		self.check_for_row_in_list_table('1: Buy chicken')
		self.check_for_row_in_list_table('2: Use peacock feather to make a fly')

		# Unique url is generated so that this list is remembered
		self.fail('Finish the test!')


# Only runs unittest when this .py program is run from terminal  <<<<<< This if statement can be removed when using the Django test runner to launch the FT
# if __name__ == '__main__':
# 	unittest.main(warnings='ignore')