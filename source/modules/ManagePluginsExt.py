import os

class ManagePluginsExt:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def Saveplugin(self, pluginComp):
		fileNames = []
		for (path, dirs, files) in os.walk(self.PluginDirectory):

			fileNames.extend(files)
		
		pluginPath = self.PluginDirectory + '/' +  pluginComp.name + self.FullExtension
		pluginName =  pluginComp.name
		
		if  pluginComp.name + self.FullExtension in fileNames:
			confirm = ui.messageBox(	'Plugin exists in folder', 
										'Plugin ' + pluginName + ' has been previously saved.', 
										buttons = ['Replace', 'Cancel'])
			if confirm != 0:
				return False
			
		pluginComp.save(pluginPath)
		
		return False

	def Saveallplugins(self):
		print('SaveAllPlugins')

		fileNames = []
		for (path, dirs, files) in os.walk(self.PluginDirectory):

			fileNames.extend(files)

		allPlugins = self.ownerComp.findChildren(tags = ['plugin'])

		skipAll = False
		replaceAll = False


		for plugin in allPlugins:

			pluginCOMP = plugin.parent()
			pluginPath = self.PluginDirectory + '/' + pluginCOMP.name + self.FullExtension
			pluginName = pluginCOMP.name

			if pluginName != 'noClip':

				if pluginCOMP.name + self.FullExtension in fileNames and not skipAll and not replaceAll:

					confirm = ui.messageBox(	'Plugin exists in folder', 
												'Plugin ' + pluginName + ' has been previously saved.', 
												buttons = ['Replace', 'Replace All', 'Skip', 'Skip All',])

					if confirm == 0:
				
						print('Replace:', pluginName)
						pluginCOMP.save(pluginPath)

					elif confirm == 1:

						print('Replace All')
						print('Replace:', pluginName)
						pluginCOMP.save(pluginPath)
						replaceAll = True

					elif confirm == 3:

						print('Skip All')
						skipAll = True

					else:

						print('Skip:', pluginName)

				elif pluginCOMP.name + self.FullExtension not in fileNames: 
					
					print('save:', pluginName)
					pluginCOMP.save(pluginPath)	


				else:

					if not skipAll:

						if replaceAll and op(pluginName):

							print('Replace:', pluginName)
							pluginCOMP.save(pluginPath)

						else:

							print('save:', pluginName)

							pluginCOMP.save(pluginPath)

					else:

						print('skip:', pluginName)
	
	def Loadplugin(self, FileName = None, PluginDir = None, FullPath = None):
		
		if FullPath is not None:
			pluginPath = FullPath
		
		elif FileName is None:
			alert = ui.messageBox("Error", "You must supply a Full Path or a FileName")
		
		elif PluginDir is None:
			pluginPath = self.PluginDirectory + '/' + FileName
		
		try:	
			self.ownerComp.loadTox(pluginPath)
		except:
			alert = ui.messageBox("Error", "Plugin does not exist in " + pluginPath)
		
		
	def Loadallplugins(self):
		print('LoadAllPlugins')

		fileNames = []
		for (path, dirs, files) in os.walk(self.PluginDirectory):

			fileNames.extend(files)

		skipAll = False
		replaceAll = False
	

		for fileName in fileNames:

			pluginName = fileName.replace(self.PluginFilePreExtension, '')
			pluginPath = self.PluginDirectory + '/' + fileName



			if self.ownerComp.op(pluginName) and not skipAll and not replaceAll:

				confirm = ui.messageBox(	'Plugin exists in project', 
											'Plugin ' + pluginName + ' is already loaded.', 
											buttons = ['Replace', 'Replace All', 'Skip', 'Skip All',])

				if confirm == 0:
			
					print('Replace:', pluginName)
					self.ownerComp.op(pluginName).destroy()
					self.ownerComp.loadTox(pluginPath)	

				elif confirm == 1:

					print('Replace All')
					print('Replace:', pluginName)
					self.ownerComp.op(pluginName).destroy()
					self.ownerComp.loadTox(pluginPath)	
					replaceAll = True

				elif confirm == 3:

					print('Skip All')
					skipAll = True

				else:

					print('Skip:', pluginName)


			elif not self.ownerComp.op(pluginName): 

					print('load:', pluginName)
					self.ownerComp.loadTox(pluginPath)	

			else:

				if not skipAll:

					if replaceAll and op(pluginName):

						print('Replace:', pluginName)
						self.ownerComp.op(pluginName).destroy()
						self.ownerComp.loadTox(pluginPath)	

					else:

						print('load:', pluginName)

						self.ownerComp.loadTox(pluginPath)	

				else:

					print('skip:', pluginName)

	def Removeallplugins(self, confirmFirst = True):
		print('DeleteAllPlugins')
		
		if confirmFirst:
			confirm = ui.messageBox(	'Remove all Plugins from Project', 
										'Are you sure? This will remove all plugins from ' + self.ownerComp.name, 
										buttons = ['Cancel', 'Removal All',])
		else:
			confirm = 1 

		if confirm == 1:

			allPlugins = self.ownerComp.findChildren(tags = ['plugin'])

			for plugin in allPlugins:

				print(plugin)

				pluginCOMP = plugin.parent()

				if pluginCOMP.name != 'noClip':

					pluginCOMP.destroy()

	def Rebuildallcontrols(self):

		allControls = self.ownerComp.findChildren(tags = ['pluginControls'])

		for controls in allControls:

			controls.Createcompui()

	@property
	def PluginDirectory(self):
		return self.ownerComp.par.Plugindirectory.eval()

	@property
	def PluginFilePreExtension(self):
		return '.' + self.ownerComp.par.Plugintype.eval()

	@property
	def FullExtension(self):
		return self.PluginFilePreExtension + '.tox'	
		


