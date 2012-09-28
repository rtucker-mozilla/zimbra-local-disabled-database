#!/usr/bin/python
from optparse import OptionParser
from zimbra_closed_accounts import ZimbraList, ZimbraAccount
if __name__ == '__main__':
	parser = OptionParser()
	usage = "usage: %prog [options] arg1 arg2"
	parser = OptionParser(usage=usage)
	parser.add_option("-p", "--list",
					  action="store_true", dest="list", default=False,
					  help="List from zimbra database")
	parser.add_option("-l", "--local-list",
					  action="store_true", dest="local_list", default=False,
					  help="List from local database")
	parser.add_option("-a", "--add",
					  action="store_true", dest="add", default=False,
					  help="Add records from zimbra database to local")
	parser.add_option("-d", "--delete",
					  action="store", dest="delete", default='',
					  help="Delete from local database")
	parser.add_option("-q", "--quiet",
					  action="store_false", dest="verbose",
					  help="be vewwy quiet (I'm hunting wabbits)")
	(options, args) = parser.parse_args()

	if options.list:
		for entry in ZimbraList().build_list():
			if entry != '':
				print entry

	if options.delete:	
		ZimbraAccount().delete(options.delete)

	if options.local_list:
		accounts = ZimbraAccount().list()
		if accounts:
			for entry in accounts:
				if entry != '':
					date_added = entry[1].split()[0]
					print "%s Created on %s" %( entry[0], date_added)

	if options.add:
		for entry in ZimbraList().build_list():
			if entry != '':
				ZimbraAccount().save(entry)


