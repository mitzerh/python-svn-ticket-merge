import sys, re
import modules.MergeRevision as svnmerge

# FFF
#REPO = "/drupal7.foxnews.com.on-air.fox-and-friends-first"
#LOCAL = "/DRUPAL-drupal7.foxnews.com.on-air.fox-and-friends-first"
# WEEKLY = "/branches/weekly_012813/"
#WEEKLY = "/trunk/"

# foxnews.com
REPO = "/foxnews.com"
LOCAL = "/DRUPAL-foxnews.com"
WEEKLY = "/branches/weekly_052713/"

# foxbusiness.com
#REPO = "/foxbusiness.com"
#LOCAL = "/DRUPAL-foxbusiness.com"
#WEEKLY = "/branches/weekly_052713/"

# nation.foxnews.com
#REPO = "/drupal7.nation.foxnews.com"
#LOCAL = "/drupal7.nation.foxnews.com"
#WEEKLY = "/branches/weekly_040113"

config = {
	
	# regex of your search on the comment block
	"search_term": re.compile(r'[A-Z]+\-[0-9]+'),
	
	"drupal": REPO,

	"svn_env": {
		"trunk": "/trunk/",
		"mq": WEEKLY,
		"prod": "/branches/production/"
	},

	"svn_location": {
		"repo": "svn+ssh://mabesah@linuxdev3.lan.tpa.foxnews.com/usr/local/svn/drupal-repos",
		"local": "/Users/mabesa/Development/Eclipse/workspace" + LOCAL
	},

	"temp_folder": "/Users/mabesa/Sites/python/svn/tmp/"

}

# start
svn = svnmerge.MergeRevision(config)
svn.setArgs()

# sample call:
# python merge.py --range=6443:6443
# python merge.py --range=6400:6443 --ticket=FOX-32324 --merge=prod


