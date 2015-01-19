from selenium import webdriver
import unittest

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
