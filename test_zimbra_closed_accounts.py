#!/usr/bin/python

import unittest
from zimbra_closed_accounts import ZimbraAccount, ZimbraAccount
import os
import datetime

class testZimbraAccount(unittest.TestCase):
	database_file = 'test_database.sqlite'
	test_email = 'test@mozilla.com'

	def setUp(self):
		"""
			Delete the test database if exists
			initialize the ZimbraAccount object for use throughout testing
		"""
		if os.path.exists(self.database_file):
			os.unlink(self.database_file)
		self.za = ZimbraAccount(self.database_file)

	def test1_constructor(self):
		"""
			Make sure that our constructor functions properly
		"""
		self.assertNotEqual(self.za, None)

	def test2_database_file_exists(self):
		"""
			Confirm that the auto creation is working correctly
		"""
		self.assertEqual(self.za._check_database_exists(self.database_file), True)
		

	def test3_save(self):
		"""
			Simple test of save
		"""
		tmp = ZimbraAccount(self.database_file).save(self.test_email)
		self.assertEqual(tmp.id, 1)

	def test4_save_and_retrieve(self):
		"""
			Simple test of save and retrieve
		"""
		ZimbraAccount(database_file=self.database_file).save(self.test_email)
		tmp = ZimbraAccount(database_file=self.database_file).get_by_email(self.test_email)
		self.assertEqual(tmp.id, 1)
		self.assertEqual(tmp.email_address, self.test_email)

	def test5_save_and_retrieve(self):
		"""
			Create the test account
			Confirm it saves correctly
			Upate the account to a new email address and confirm the save
		"""

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
			This shouldn't do anything really other than create one entry
			It should create just one entry.
			Just confirming no exception tossed
		"""
		ZimbraAccount(database_file=self.database_file).save(self.test_email)
		self.assertEqual(ZimbraAccount(database_file=self.database_file).count(), 1)
		ZimbraAccount(database_file=self.database_file).save(self.test_email)
		self.assertEqual(ZimbraAccount(database_file=self.database_file).count(), 1)

	def test7_delete_by_email(self):
		"""
			Create the test account and delete
		"""
		ZimbraAccount(database_file=self.database_file).save(self.test_email)
		self.assertEqual(ZimbraAccount(database_file=self.database_file).count(), 1)
		ZimbraAccount(database_file=self.database_file).delete(self.test_email)
		should_be_gone = ZimbraAccount(database_file=self.database_file).get_by_email(self.test_email)
		self.assertEqual(should_be_gone, None)
		self.assertEqual(ZimbraAccount(database_file=self.database_file).count(), 0)

	def test8_count(self):
		"""
			As an additional sanity check lets do the following:
			1. Add the same test account, this should succeed
			2. Add the same test account again, this should fail
			3. Add a new test account, this should succeed
		"""

		ZimbraAccount(database_file=self.database_file).save(self.test_email)
		ZimbraAccount(database_file=self.database_file).save(self.test_email)
		ZimbraAccount(database_file=self.database_file).save('test2@mozilla.com')
		record_count = ZimbraAccount(database_file=self.database_file).count()
		self.assertEqual(record_count, 2)

if __name__ == '__main__':
	unittest.main()
