import sys, getopt, subprocess, re

# set
def set(config):
	return MergeRevision(config)


class MergeRevision:
	
	def __init__(self, config):
		
		# get arguments
		self.__ARGS = sys.argv[1:]
		
		# constants
		self.__CONST = {}

		self.__CONST['drupal_repo'] = config["drupal"] if "drupal" in config else ""

		self.__CONST['temp_path'] = config["temp_folder"] if "temp_folder" in config else 0

		self.__CONST['svn_env'] = config["svn_env"]

		self.__CONST['svn_location'] = config["svn_location"]

		self.__CONST['search_term'] = config["search_term"]
	
	def setArgs(self, arguments = None):
		
		if arguments == None:
			arguments = self.__ARGS
	
		svn_location = self.__CONST['svn_location']
		svn_env = self.__CONST['svn_env']
		drupal = self.__CONST['drupal_repo']
		config = {}

		try:
			options, args = getopt.getopt(arguments,'lML',['mergeTo=','range=','ticket=','path='])
		except getopt.GetoptError:
			self.__getOut()


		for opt, arg in options:
			if opt == '-l':
				config['svn_log'] = 1
			if opt == '-L':
				config['svn_latest_commit_only'] = 1
			if opt == '-M':
				config['svn_run_merge'] = 1

			if opt == '--range':
				config['svn_rng'] = arg

			if opt == '--ticket':
				config['svn_ticket'] = arg

			if opt == '--mergeTo':
				config['svn_env'] = arg

			if opt == '--path':
				config['svn_path'] = arg
		
		if not all (k in config for k in ("svn_rng","svn_ticket","svn_env")):
			self.__getOut()
		
		if config['svn_env'] == 'qa':

			env_str = svn_location['repo'] + drupal + svn_env['trunk']

		elif config['svn_env'] == 'prod':

			env_str = svn_location['repo'] + drupal + svn_env['qa']

		else:
			self.getOut()
		
		
		# if there is a path
		if 'svn_path' in config:
			env_str = env_str + config['svn_path']
			
		# build command string
		cmd_args = ['svn','log','-v','-r' + config['svn_rng']]
		
		# append environment
		cmd_args.append(env_str)
		
		cmd_str = ' '.join(cmd_args)
		
		print 'Running.. '
		print cmd_str

		#print cmd_str
		#subprocess.call(cmd_str, shell=True)

		cmd = subprocess.Popen(cmd_args, stdout=subprocess.PIPE)
		cmd_out, cmd_err = cmd.communicate()

		if len(cmd_out) > 0:
			print 'Parsing.. '
			#setString(cmd_out,ticket,env,log,path)
			self.__setString(cmd_out, config)
		else:
			print 'No Output..'

		print 'Done.'

	#eof setArgs
	
	def __setString(self, svn_str, config):
		
		new_arr = []
		selected_arr = []
		
		ticket = config['svn_ticket']
		env = config['svn_env']
		path = config['svn_path'] if 'svn_path' in config else 0
		log = config['svn_log'] if 'svn_log' in config else 0
		latest_only = config['svn_latest_commit_only'] if 'svn_latest_commit_only' in config else 0
		temp_path = self.__CONST['temp_path']
		
		
		svn_location = self.__CONST['svn_location']
		svn_env = self.__CONST['svn_env']
		drupal = self.__CONST['drupal_repo']

		# parse!
		# 1. separate each commit
		new_str = re.sub(r'(\-{10,})([\n\r]+)', "BREAK\n\n", svn_str)
		arr = new_str.split("BREAK\n\n")

		if len(arr) > 0:
			
			# clean out array - trim and remove blanks
			for val in arr:
				tmp = val.strip()
				if (len(tmp) > 0):
					new_arr.append(tmp)
			
			
			# set up the ticket info
			if len(new_arr) > 0:
				for i,val in enumerate(new_arr):
					tmp_log_data =  self.__setLogData(val)

					if tmp_log_data:
						new_arr[i] = tmp_log_data

						if (self.__isTicket(ticket, new_arr[i]["ticket"])):
							selected_arr.append(new_arr[i])

			#enf if

		#end if

		if len(selected_arr) > 0:

			if env == 'prod':
				merge_from = svn_location['repo'] + drupal + svn_env['qa']
				merge_to = svn_location['local'] + svn_env['prod']
			else:
				merge_from = svn_location['repo'] + drupal + svn_env['trunk']
				merge_to = svn_location['local'] + svn_env['qa']

			# if there's a path, append
			if path:
				merge_from = merge_from + path
				merge_to = merge_to + path
			
			svn_merge_cmd = 'svn merge --ignore-ancestry -c{revisions} ' + merge_from + ' ' + merge_to

			revs = None
			rev_arr = []

			for val in selected_arr:
				rev_arr.append(val['revision'])

			if len(rev_arr) > 0:

				if latest_only:
					revs = rev_arr[len(rev_arr) - 1]
				else:
					revs = ','.join(rev_arr)

				svn_merge_cmd = svn_merge_cmd.replace('{revisions}',revs)

			print 'Merge revisions found!!'

			if log:
				
				if not temp_path:
					print 'Requries temp folder path!!'
				else:
					print 'TODO: Generating log file at ' + temp_path + '...'
					#TODO:
					#saveToFile(svn_merge_cmd,selected_arr)

			else:
				
				print 'Generating command line:'
				print svn_merge_cmd
				
				#if 'svn_run_merge' in config and config['svn_run_merge']:
				#	merge_prompt = 1
				#else:
				#	merge_prompt = self.__sysPrompt('Do You want to execute the svn merge?')

				#if merge_prompt:
				#	print 'Running SVN Merge...\n'
				#	cmd = subprocess.Popen(svn_merge_cmd.split(' '), stdout=subprocess.PIPE)
				#	cmd.stdout.readline()

		else:

			print 'No merge revisions found.'

		#end if	

		#print selected_arr[0]
		#print new_arr[0]
		
	#eof setString	
	
	
	def __setLogData(self, arr_str):
		
		search_term = self.__CONST['search_term']

		obj = {}

		# 1. get revision, username, and timestamp line
		line = re.search(r'.+',arr_str)

		if line != None:
			
			# split by pipes
			tmp = (line.group(0)).split("|")

			for i,val in enumerate(tmp):
				# trim
				val = val.strip()
				#revision
				if (i == 0):
					obj['revision'] = val[1:]
				#user
				if (i == 1):
					obj['user'] = val
				#timestamp
				if (i == 2):
					obj['timestamp'] = val
				if (i == 3):
					obj['lines'] = val
			#endfor

		# get ticket number
		try:
			# comment string
			sp = arr_str.split('\n')
			comment_str = sp[len(sp) - 1]
			ticket_arr = re.findall(search_term, comment_str)
			obj['ticket'] = ticket_arr
		except:
			ticket_arr = 0
		
		if ticket_arr:
			# get comment
			try:
				
				tix = ticket_arr[len(ticket_arr)-1]
				sp = comment_str.split(tix)
				
				comment_str = sp[1] if len(sp) > 1 else comment_str
				
				if (len(comment_str) == 0):
					comment_str = '<NO COMMENT>'
				
				obj['log'] = comment_str
				
			except:
				print "Error while trying to get comment:", sys.exc_info()[0]
				sys.exit()
			
			# change paths
			idx_start = re.search(r'\bChanged paths:',arr_str).start();
			idx_end = re.search(ticket_arr[0],arr_str).start();
			
			change_str = arr_str[int(idx_start):int(idx_end)]
			change_str = re.sub(r'\bChanged paths:','',change_str);
			change_str = change_str.strip()
			
			change_arr = change_str.split('\n')

			for i, val in enumerate(change_arr):
				change_arr[i] = val.strip()

			obj['changes'] = change_arr
			
		else:
			obj = 0
		
		return obj
	#eof setLogData
	
	# check if valid ticket
	def __isTicket(self, ticket, search):
		arr = ticket.split(',')
		valid = 0

		for val in arr:

			if type(search) is list:

				if val in search:
					valid = 1
					break

			else:

				if val == search:
					valid = 1
					break

		#end for

		return valid
	#eof isTicket
	
	def __sysPrompt(self, prompt_str):
		sys.stdout.write(prompt_str + ' [y/n]: ')
		choice = raw_input().lower()
		
		if choice == 'y' or choice == 'yes':
			ret = 1
		else:
			ret = 0
		return ret	
	#eof sysPrompt
		
	
	def __getOut(self):
		p_str = 'usage: merge-log.py [ -l | -L ] --range=<revision>:<revision> --ticket=<ticket> --mergeTo=<qa|prod>'
				

		sys.exit(2)
	#eof getOut

#eoc SvnMergeRevision
