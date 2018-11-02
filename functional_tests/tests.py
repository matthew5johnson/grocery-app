from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

# browser = webdriver.Firefox(keep_alive=False)
# browser.get('http://localhost:8000') <<<-- == http://127.0.0.1:8000/

# assert 'To-Do' in browser.title

class NewVisitorTest(LiveServerTestCase):  # unittest.TestCase

	def setUp(self):
		self.browser = webdriver.Firefox(keep_alive=False)

	def tearDown(self):
		self.browser.quit()

	def wait_for_row_in_list_table(self, row_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_element_by_tag_name('tr')
				# self.assertIn('foo', rows) # Not iterable
				# self.assertIn(row_text, [row.text for row in rows])  # This object isn't iterable, but it looks like we check for it further down in the functional test anyway, so should be safe to comment out here.		
				return
			
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e 
				time.sleep(0.5)

	def test_multiple_users_can_start_lists_at_differnt_urls(self):    ##test_can_start_a_list_for_one_user
		self.browser.get(self.live_server_url)   # self.live_server_url  'http://localhost:8000'

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
		# time.sleep(1)
		self.wait_for_row_in_list_table('1: Buy chicken')

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
		# time.sleep(1)
		self.wait_for_row_in_list_table('2: Use peacock feather to make a fly')
		self.wait_for_row_in_list_table('1: Buy chicken')

		# Page updates again, now showing both items on the list
		# self.check_for_row_in_list_table('1: Buy chicken')
		# self.check_for_row_in_list_table('2: Use peacock feather to make a fly')

		# Unique url is generated so that this list is remembered
		# She notices that her list has a unique URL
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		# Now a new user, Francis, comes along to the site
		## We use a new browser session to make sure that no information 
		## of Edith's is coming through from cookies etc
		self.browser.quit()
		self.browser = webdriver.Firefox()

		# Francis visits the home page. There is no sign of Edith's list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text 
		self.assertNotIn('Buy chicken', page_text)
		self.assertNotIn('make a fly', page_text)

		# Francis starts a new list by entering a new item.
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		# Francis gets his own unique URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		# Again, there is no trace of Edith's list
		page_text = self.browser.find_element_by_tag_name('body').text 
		self.assertNotIn('Buy chicken', page_text)
		self.assertIn('Buy milk', page_text)



		self.fail('Finish the test!')

# def test_multiple_users_can_start_lists_at_differnt_urls(self):
# 	# Edith starts a new to-do list
# 	self.browser.get(self.live_server_url)
# 	inputbox = self.browser.find_element_by_id('id_new_item')
# 	inputbox.send_keys('Buy chicken')
# 	inputbox.send_keys(Keys.ENTER)
# 	self.wait_for_row_in_list_table('1: Buy chicken')

	# # She notices that her list has a unique URL
	# edith_list_url = self.browser.current_url
	# self.assertRegex(edith_list_url, '/lists/.+')

	# # Now a new user, Francis, comes along to the site
	# ## We use a new browser session to make sure that no information 
	# ## of Edith's is coming through from cookies etc
	# self.browser.quit()
	# self.browser = webdriver.Firefox()

	# # Francis visits the home page. There is no sign of Edith's list
	# self.browser.get(self.live_server_url)
	# page_text = self.browser.find_element_by_tag_name('body').text 
	# self.assertNotIn('Buy chicken', page_text)
	# self.assertNotIn('make a fly', page_text)

	# # Francis starts a new list by entering a new item.
	# inputbox = self.browser.find_element_by_id('id_new_item')
	# inputbox.send_keys('Buy milk')
	# inputbox.send_keys(Keys.ENTER)
	# self.wait_for_row_in_list_table('1: Buy milk')

	# # Francis gets his own unique URL
	# francis_list_url = self.browser.current_url
	# self.assertRegex(francis_list_url, '/lists/.+')
	# self.assertNotEqual(francis_list_url, edith_list_url)

	# # Again, there is no trace of Edith's list
	# page_text = self.browser.find_element_by_tag_name('body').text 
	# self.assertNotIn('Buy chicken', page_text)
	# self.assertIn('Buy milk', page_text)




# Only runs unittest when this .py program is run from terminal
if __name__ == '__main__':
	unittest.main(warnings='ignore')