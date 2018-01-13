def CreateNodeFiles(srcFile, numMachines, numGPUs, uiMachine, uiGPU):
	
	# numCards is a list of # of GPUs of each machine
	
	confirm = ui.messageBox('Create Node Files', 'Are you sure? This will overwrite previous node files.', buttons = ['Yes', 'No'])
	
	if confirm == 0:
	
		projectFolder = project.folder
		projectPath = projectFolder + '/' + srcFile
		
		name = ''
		
		from shutil import copyfile as copyFile
						
		for i in range(0, numMachines):

			UIGPU = [-1, uiGPU][i == 0 and uiMachine == 1]

			for n in range(0, numGPUs[i]):
			
				if n != UIGPU:
					name = 'M' + str(i) + '_GPU' + str(n) + '.toe'	
					copyFile(projectPath, name)
				


def LoadLocal(projectName, node = 'node0', server = 0, gpu = -1):

	#if not (op.DATABASE.fetch('PREVIEW_NODE') == 'master' and node == 'node0'):

		binFolder = app.binFolder
		binFolder = re.sub('[/]', '\\\\', binFolder)

		projectFolder = project.folder
		projectFolder = re.sub('[/]', '\\\\', projectFolder)
		#projectFolder = '"' + projectFolder + '"'

		projectPath = '"' + projectFolder + '\\' + projectName + '"'
		
		exeName = 'touchdesigner099.exe'

		if gpu != -1:
			arg0 = ' -gpuformonitor ' + str(gpu * 4) + ' '
			launchCommand = exeName + arg0
		else:
			launchCommand = exeName + ' '

		pOpenCommand = launchCommand + projectPath

		envV = mod.os.environ
		envV["NODE"] = str(node)
		envV["SERVER"] = str(server)
		envV["GPU"] = str(gpu)

		p = mod.subprocess.Popen(pOpenCommand, cwd = binFolder, env=envV)

	#print(p.pid)

def StopLocal(pid):
	
	try:
		mod.os.kill(pid, 0)
	except:
		pass

def rawStr(string):
	rStr = "%r"%string
	return rStr[1:-1]

def LoadRemote(client, userName, password, projectName, node = 'node0', server =0, gpu =-1):

	masterIP = me.fetch('MASTER_IP')

	binFolder = app.binFolder
	binFolder = re.sub('[/]', '\\\\', binFolder)

	projectDir = project.folder
	projectDir = re.sub('[/]', '\\\\', projectDir)
	lmDir = projectDir.replace('\\project', '\\assets')
	projectFolder = projectDir.replace(':', '') 
	projectFolder = '"\\\\' + masterIP + '\\' + projectFolder 
	projectPath = projectFolder + '\\' + projectName
		
	exeName = 'touchdesigner099.exe'
	if gpu != -1:
		arg0 = ' -gpuformonitor ' + str(gpu * 4) + ' '
		launchCommand = exeName + '" ' + arg0
	else:
		launchCommand = exeName + '" '
	
	launchCommand = '"'+ binFolder + '\\' + launchCommand + projectPath + '"'

	psCommand = 'cmd /c set SERVER='+ str(server) +'& set GPU='+ str(gpu) +'& set NODE='+ str(node) +'& ' + launchCommand	
	dirExe = rawStr(lmDir + '\externalTools\PSTools\PsExec.exe -d -i \\')
	rDir = rawStr(lmDir + '\externalTools\PSTools')
	UserName = rawStr(userName)
	pOpenCommand = dirExe + client +' -u '+ UserName +' -p '+ password +' '+ psCommand	
	
	#p = mod.subprocess.Popen(pOpenCommand, cwd = rDir)

	index = int(node.replace('node', ''))

	run("mod.subprocess.Popen(args[0], cwd = args[1])", pOpenCommand, rDir, delayFrames = 15 * index)

	print('Launching:\t', node, '\n\t\t\t', 'On Server ', server, '\n\t\t\t', 'GPU ', gpu,
	'\n\t\t\t', 'File ', projectName, '\n\t\t\t', 'Project Path ', projectPath,
	'\n\t\t\t', 'pOpenCommand ', pOpenCommand,
	'\n\t\t\t', 'Launch Command ', launchCommand)


def StopRemote(client, userName, password, pid):

	command = r'C:\PSTools\pskill.exe \\'+ client +' -u '+ userName +' -p '+ password + ' ' + str(pid)

	mod.subprocess.Popen(command, cwd = r"C:\PSTools")

