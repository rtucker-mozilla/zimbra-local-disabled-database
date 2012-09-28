#!/usr/bin/python

import unittest
from zimbra_closed_accounts import ZimbraAccount, ZimbraList
import os
import datetime

class testZimbraList(unittest.TestCase):
	test_return = """test@mozilla.com\ntest2@mozilla.com\ntest3@mozilla.com"""

	def setUp(self):
		pass

	def test1_test_return_list(self):
		ret = ZimbraList().return_list(self.test_return)
		self.assertEqual(len(ret), 3)
		self.assertEqual(ret[0], 'test@mozilla.com')
		self.assertEqual(ret[1], 'test2@mozilla.com')
		self.assertEqual(ret[2], 'test3@mozilla.com')

	def test2_test_actual_data(self):
		ret = ZimbraList().return_list()
		self.assertNotEqual(len(ret), 0)
		self.assertTrue('' not in ret)

		

if __name__ == '__main__':
	unittest.main()
