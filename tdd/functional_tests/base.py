from selenium import webdriver
#import unittest
#from selenium.webdriver.common.keys import Keys
#import time
import sys
#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            #print "arg", arg
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                #print "Server URL", cls.server_url
                return
            else:
                cls.server_url = 'http://localhost:8000'
                return
        #super(FunctionalTest, cls).setUpClass()
        #cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super(NewVisitorTest, cls).tearDownClass()

    def setUp(self):
        self.browser = webdriver.Firefox()
    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

