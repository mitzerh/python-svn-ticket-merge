import sys, re
import modules.MergeRevision as svnmerge

REPO = "/live.foxnews.com-responsive"
LOCAL = "/GFX-live.foxnews.com-responsive"
TRUNK = "/trunk/"
WEEKLY = "/production"
PROD = "/branches/production/"

#REPO = "/video.foxnews.com"
#LOCAL = "/GFX-video.foxnews.com"
#TRUNK = "/branches/responsive"
#WEEKLY = "/responsive"
#PROD = "/branches/responsive-prod"

#REPO = "/trending.foxnews.com"
#LOCAL = "/GFX-trending.foxnews.com"
#TRUNK = "/trunk"
#WEEKLY = "/weekly_022513"
#PROD = "/branches/production"


config = {
	
	# regex of your search on the comment block
	"search_term": re.compile(r'[A-Z]+\-[0-9]+'),
	
	"drupal": REPO,

	"svn_env": {
		"trunk": TRUNK,
		"mq": "/branches"+WEEKLY+"/",
		"prod": PROD
	},

	"svn_location": {
		"repo": "svn+ssh://mabesah@linuxdev3.lan.tpa.foxnews.com/usr/local/svn/gfx-repos",
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


