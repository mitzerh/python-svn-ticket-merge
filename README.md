python-svn-ticket-merge
=======================

A simple python script for an extended SVN merge for revisions with a ticketing system type of logging.
This will generate a svn merge command for you to run.

Sample commit with ticketing log
--------------------------------

	svn ci -m "TICKET-32324 : Updates to this project"
&nbsp;

Sample calls
------------
	
**Merging all commits QA branch (branch revision from TRUNK to QA)**

	python merge.py --range=8000:9000 --ticket=TICKET-32324 --mergeTo=qa
&nbsp;

**Merging all commits PROD branch (branch revisions from QA to PROD)**

	python merge.py --range=8000:HEAD --ticket=TICKET-32324 --mergeTo=prod
&nbsp;

**Merge only your latest commit***

	python merge.py --range=8000:HEAD --ticket=TICKET-32324 --mergeTo=prod -L
&nbsp;

**Merge multiple tickets (comma separated)**

	# python merge.py --range=8000:9000 --ticket=TICKET-123,TICKET-45678,TICKET-90112,TICKET-32324 --mergeTo=qa
&nbsp;

