
# An extended SVN merge which is useful for commits using a ticketing system

# sample call:
# merging to QA branch (branch revision from TRUNK to QA)
# python merge.py --range=8000:9000 --ticket=TICKET-32324 --mergeTo=qa

# merging to PROD branch (branch revisions from QA to PROD)
# python merge.py --range=8000:HEAD --ticket=TICKET-32324 --mergeTo=prod
 
# merge multiple tickets (comma separated)
# python merge.py --range=8000:9000 --ticket=TICKET-123,TICKET-45678,TICKET-90112,TICKET-32324 --mergeTo=qa


import sys, re
import modules.MergeRevision as TicketMerge

config = {
	
	# regex of your search on the comment block
	# customize based on your ticketing system
	"search_term": re.compile(r'[A-Z]+\-[0-9]+'),

	# branch locations
	# "trunk" - your DEVELOPMENT
	# "mq" - QA branch
	# "prod" - PROD branch
	"svn_env": {
		"trunk": "/trunk/",
		"qa": "/branch/current-QA/",
		"prod": "/branch/current-PROD/"
	},

	# repo locations
	# "repo" - your repo path
	# "local" - your local repo path
	"svn_location": {
		"repo": "svn+ssh://hmabesa@repo.location.mysamplerepo.com/svn/projects",
		"local": "/Users/hmabesa/Development/workspace/projects"
	},

	# just somewhere to dump logs  
	"temp_folder": "/Users/hmabesa/tmp/"

}

# start
svn = TicketMerge.set(config)
svn.setArgs()