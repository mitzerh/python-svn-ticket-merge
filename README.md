python-svn-ticket-merge
=======================

A simple python script for an extended SVN merge for revisions with a ticketing system type of logging


Sample calls
------------
	
**Merging to QA branch (branch revision from TRUNK to QA)**

	python merge.py --range=8000:9000 --ticket=TICKET-32324 --mergeTo=qa
&nbsp;

**Merging to PROD branch (branch revisions from QA to PROD)**

	python merge.py --range=8000:HEAD --ticket=TICKET-32324 --mergeTo=prod
&nbsp;

**Merge multiple tickets (comma separated)**

	# python merge.py --range=8000:9000 --ticket=TICKET-123,TICKET-45678,TICKET-90112,TICKET-32324 --mergeTo=qa
&nbsp;