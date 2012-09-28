#!/usr/bin/python

import unittest
from zimbra_closed_accounts import ZimbraAccount, ZimbraAccount
import os
import datetime

class testZimbraAccount(unittest.TestCase):
	database_file = 'test_database.sqlite'
	test_email = 'test@mozilla.com'

	def setUp(self):
		if os.path.exists(self.database_file):
			os.unlink(self.database_file)
		self.za = ZimbraAccount(self.database_file)

	def test1_constructor(self):
		self.assertNotEqual(self.za, None)

	def test2_database_file_exists(self):
		self.assertEqual(self.za._check_database_exists(self.database_file), True)
		

	def test3_save(self):
		tmp = ZimbraAccount(self.database_file).save(self.test_email)
		self.assertEqual(tmp.id, 1)

	def test4_save_and_retrieve(self):
		ZimbraAccount(database_file=self.database_file).save(self.test_email)
		tmp = ZimbraAccount(database_file=self.database_file).get_by_email(self.test_email)
		self.assertEqual(tmp.id, 1)
		self.assertEqual(tmp.email_address, self.test_email)

	def test5_save_and_retrieve(self):
		ZimbraAccount(database_file=self.database_file).save(self.test_email)
		new_save = ZimbraAccount(database_file=self.database_file).get_by_email(self.test_email)
		new_save.email_address = 'newemail@mozilla.com'
		new_save.save()
		new_ret = ZimbraAccount(database_file=self.database_file).get_by_email('newemail@mozilla.com')
		self.assertEqual(new_ret.id, 1)
		self.assertEqual(new_ret.email_address, 'newemail@mozilla.com')
		should_be_gone = ZimbraAccount(database_file=self.database_file).get_by_email(self.test_email)
		self.assertEqual(should_be_gone, None)

	def test6_save_duplicate(self):
		"""
			This shouldn't do anything really
			Just confirming no exception tossed
		"""
		ZimbraAccount(database_file=self.database_file).save(self.test_email)
		ZimbraAccount(database_file=self.database_file).save(self.test_email)

if __name__ == '__main__':
	unittest.main()
