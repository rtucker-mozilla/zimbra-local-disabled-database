#!/usr/bin/python
import sqlite3 
import ldap 
import os
import datetime
import subprocess

class ZimbraList:
	list_command = [
		'zmprov',
		'sa',
		'&(objectClass=zimbraAccount)(zimbraAccountStatus=*closed*)',
		]
	def __init__(self):
		pass

	def return_list(self, return_list=None):
		"""
			Return the list of accounts maching search criteria
			as definied in self.list_command
		"""
		return self.build_list(return_list)

	def build_list(self, return_list=None):
		"""
			Accept optional return_list argument for testing
			if return_list is specificied set the output to it
		"""
		if return_list:
			output = return_list
		else:
			"""
				Create the list of accounts matching criteria
			"""
			p = subprocess.Popen(
				self.list_command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			output, errors = p.communicate()
		return self.sanitize_output(output)

	def sanitize_output(self, input):
		input = input.strip().split("\n")
		tmp = []
		for i in input:
			if i != '':
				tmp.append(i)
		return tmp
		

class ZimbraReport:

	def __init__(self):
		pass

class ZimbraAccount:
	database_file = "zimbra_report.sqlite"
	_database_exists = False
	conn = None
	id = None
	email_address = None
	updated_on = datetime.datetime.now()
	created_on = datetime.datetime.now()
	from_db = False

	def __init__(self, database_file=None):
		"""
			Check if a database file has been
			passed in. This will be for
			testing
			
		"""
		if database_file:
			self.database_file = database_file
			"""
				Entry point to tell if we're testing
				If we're providing a database file
				we're testing
			"""
			db_exists = self._database_exists = self._check_database_exists(
												self.database_file)
			if not db_exists:
				self._create_initial_database(self.database_file)
			self.database_file = database_file
			self.conn = self._get_conn(self.database_file)
		else:
			self.process()

	def process(self):
		db_exists = self._database_exists = self._check_database_exists(
											self.database_file)
		if not db_exists:
			self._create_initial_database(self.database_file)

		self.conn = self._get_conn(self.database_file)
		self.get_by_email()

	def list(self):
		tmp = []
		search = "SELECT email_address, created_on from removed_accounts"
		try:
			for row in self.conn.execute(search):
				tmp.append((row[0], row[1]),)
		except UnboundLocalError:
			tmp.append('Not Found')
		return tmp

	def delete(self, email_address=None):
		deleted = False
		error_message = ""
		if not email_address:
			email_address = self.email_address
		delete_tuple = (email_address, )
		
		delete_string = "DELETE from removed_accounts where email_address = ?"
		try:
			cursor = self.conn.cursor()
			cursor.execute(delete_string, delete_tuple)
			self.conn.commit()
			deleted = True
			error_message = "Successfully Delete"
			self.id = cursor.lastrowid
		except sqlite3.IntegrityError:
			deleted = False	
			error_message = "Email Address Exists"
		return deleted, error_message

	def count(self):
		count = 0
		search = "SELECT count(*) from removed_accounts"
		cursor = self.conn.cursor()
		cursor.execute(search)
		result = cursor.fetchone()
		try:
			count = result[0]
		except TypeError:
			count = 0
		return count
				
	def save(self, email_address=None, save_time=None):
		"""
			Check to see if the email address exists currently
			in the database. If not than insert it.
		"""
		saved = False
		error_message = ""
		if not save_time:
			save_time = datetime.datetime.now()
		if email_address:
			self.email_address = email_address
			self.created_on = save_time
			self.updated_on = save_time

		record_tuple = (
						self.email_address,
						self.created_on,
						self.updated_on)
		if not self.id:
			insert_string = "INSERT into removed_accounts\
			(email_address, created_on, updated_on) values (?, ?, ?)"
			try:
				cursor = self.conn.cursor()
				cursor.execute(insert_string, record_tuple)
				self.conn.commit()
				saved = True
				error_message = "Successfully Saved"
				self.id = cursor.lastrowid
			except sqlite3.IntegrityError:
				saved = False	
				error_message = "Email Address Exists"
		else:
			update_string = "update removed_accounts set email_address = ?, created_on = ?, updated_on = ? where id = ?"
			update_tuple = (
							self.email_address,
							self.created_on,
							self.updated_on,
							self.id,
							)
			try:
				self.conn.execute(update_string, update_tuple)
				self.conn.commit()
				saved = True
				error_message = "Successfully Saved"
			except sqlite3.IntegrityError:
				saved = False	
				error_message = "Email Address Exists"

		return self

	def get_by_email(self, email_address = None, database_file = None):
		
		if email_address:
			search_address = email_address
		else:
			search_address = self.email_address
		search = "SELECT * from removed_accounts where email_address = ?"
		search_tuple = (
						search_address,
						)
		cursor = self.conn.cursor()
		cursor.execute(search, search_tuple)
		result = cursor.fetchone()
		try:
			self.id = result[0]
			self.email_address = result[1]
			self.created_on = result[2]
			self.updated_on = result[3]
			self.from_db = True
		except TypeError:
			return None
		return self

	def _check_for_record(self, email_address):
		search = "SELECT count(*) from removed_accounts\
		where email_address = ?"
		search_tuple = (
						email_address,
						)
		c = self.conn.cursor()
		c.execute(search, search_tuple)
		count_res = c.fetchone()
		return True if count_res > 0 else False
	def _get_conn(self, database_file):
		"""
			Return a connection object to
			the sqlite3 database
		"""
		self.conn = sqlite3.connect(database_file)
		return self.conn

	def _check_database_exists(self, database_file):
		return os.path.exists(database_file)

	def _create_initial_database(self, database_file):
		conn = self._get_conn(database_file)
		create_table_string = "CREATE table removed_accounts (\
		id integer PRIMARY KEY,\
		email_address VARCHAR(128) UNIQUE,\
		created_on DATE,\
		updated_on DATE)"

		res = conn.execute(create_table_string)
		"""
			create the sqlite3 database file with
			schema
		"""

	def _list_all(self, return_list=None):
		"""
			List all disabled accounts
			from the local database file
			if return_list has been passed
			just return it back out. this is for
			testing
		"""
		if return_list:
			return return_list
	
	def _search_ldap(self):
		"""
			search ldap to get the disabled and
			modified timestamp of this account
		"""
		pass
	
	def _add_accounts(self, add_account_list):
		"""
			Iterate over the list of accounts
			add them to the database if they
			do not exist along with a timestamp
			of our current operation
		"""
		pass
	
	def _insert_account(self, account):
		"""
			Do the insertion to the sqlite
			database of the account.
		"""
		pass
	
	def _create_database(self, database_file):
		"""
			create the database if it does not
			exist
		"""
		pass
	
	def _check_for_database(self, database_file):
		"""
			Check to see if the database file
			exists
		"""
		pass
