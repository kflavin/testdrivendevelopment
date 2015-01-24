from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
    def tearDown(self):
        self.browser.quit()
    def test_can_start_a_list_and_retrieve_it_later(self):
        # User goes to checkout homepage
        self.browser.get('http://localhost:8000')

        # User notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        # She types "Buy peacock feathers"
        inputbox.send_keys('Use peacock feathers to make a fly')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)

        table = self.browser.find_element_by_id('id_list_table')
        print "text of the table", table.text
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        self.assertIn('2: Use peacock feathers to make a fly', [row.text for row in rows])

        self.fail('Finish the test!')

        # User is invited to enter a to-do list item


if __name__ == '__main__':
    #unittest.main(warnings='ignore')
    unittest.main()



# User wants to check out to-do app.  goes to homepage

# User notices the title

# User is invited to enter a to-do item

# User types in their todo message, "run errands"

# User hits enter, the page updates and shows the todo item

# There is a another box to enter more items, User enter "clean house"

# Page updates again and shows both items

# User wonders if list has been saved; site generates a unique URL for user

# User visits URL to see that todo list is still there

# User satisfied, and exits
