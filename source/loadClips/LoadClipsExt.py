"""
Extension classes enhance TouchDesigner component networks with python
functionality. An extension can be accessed via ext.ExtensionClassName from
any operator within the extended component. If the extension is "promoted", all
its attributes with capitalized names can be accessed directly through the
extended component, e.g. op('yourComp').ExtensionMethod()
"""
import tableFunc as TF
import pickle

class LoadClipsExt:
	"""
	LoadClipsExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.UDT_Out = op.CONTROL_OUT.op('reliableUDT')
		self.LoadMovieComp = self.ownerComp.op('loadMovie')
		self.LoadAudioComp = self.ownerComp.op('loadAudio')
		self.DropFolderComp = self.ownerComp.op('dropFolder')

		self.videoTypes = ('mov', 'MOV', 'avi', 'AVI', 'mp4', 'MP4', 'wmv', 'WMV' 'mpg', 'mpeg', 'm4v', 'gif')
		self.imageTypes = ('tif','tiff','jpg','jpeg','bmp','png','tga', 'PNG')
		self.audioTypes = ('wav','mp3', 'aif', 'aiff', 'm4a')
		self.movTypes = self.videoTypes + self.imageTypes


	def DropMedia(self, *args):

		mediaType = args[5]
		bank = me.fetch('CUR_BANK')
		clipUIPath = args[7]
		clipUI = op(clipUIPath)

		clipPathSplit = clipUIPath.split('/')
		channel = clipPathSplit[-2:][0]
		clip = clipPathSplit[-1:][0]

		dataClipPath = me.fetch('CLIP_DATA') +'/'+ bank +'/'+ channel +'/'+ clip

		if mediaType in self.movTypes or mediaType in self.imageTypes:
			
			name = args[6]
			path = args[0]
			numItems = int(args[4])
			curId = int(args[3])
			
			if numItems == 1:
				self.LoadMovieComp.op('makeThumb').run(name, path, mediaType, bank, channel, clip)
			
			else:
			
				n2 = name.split('.')

				multiLoad = self.LoadMovieComp.op('multiLoad')
				loadList = multiLoad.fetch('LoadList', [])
				
				loadList.append([name, path, mediaType, bank, channel, clip])
				#mod.pprint.pprint(loadList)
				
				multiLoad.store('LoadList', loadList)
				multiLoad.store('NumItems', numItems)
				
				if curId == numItems - 1:
					bankOverride = 0
					multiLoad.run(bankOverride)

		elif mediaType == 'COMP':
			
			if args[0] != 'select':
				
				#check for browser drag
				name = args[0]
				if name == 'contents':

					browser = op.BROWSER
					browserContents = browser.op('contents')
					selected = browserContents.fetch('selected', [])
					selectedType = selected[0]['type']
					
					if selectedType == 'movie' or selectedType == 'image':
						mediaType = selected[0]['extension']
						
						if mediaType in self.movTypes or mediaType in self.imageTypes:
							
							name = selected[0]['basename']
							path = selected[0]['path'] + selected[0]['name']
							numItems = len(selected)
							
							if numItems == 1:
								op('loadMovie/makeThumb').run(name, path, mediaType, bank, channel, clip)
					
					elif selectedType == 'gen':
						name = selected[0]['name']
						path = selected[0]['location']
						#print(name, path, mediaType,bank,channel,clip)
						self.LoadComp(name, path, mediaType, bank, channel, clip)
	

				else:
				
					list_ = op(args[6] + '/' + args[0])
					items = list_.op('selectItems')
					listType = op(list_).fetch('ListType')
					
					if listType == 'gen':
					
						listSlot = op(list_).panel.celldragid + 1
						name = items[listSlot, 'name'].val
						path = items[listSlot, 'path'].val
						#print(name, path, mediaType,bank,channel,clip)
						self.LoadComp(name, path, mediaType,bank,channel,clip)

			else:

				#sourceClip = op(op(args[6]).fetch('DataClipPath'))
				sourceClip = op.CLIP_DATA.op(me.fetch('CUR_BANK')).op(op(args[6]).parent().name).op(op(args[6]).name)
				
				
				sourceLane = op(sourceClip.parent().path)
				sourceName = sourceClip.name
				#destClip = op(op(args[7]).fetch('DataClipPath'))
				destClip = op.CLIP_DATA.op(me.fetch('CUR_BANK')).op(op(args[7]).parent().name).op(op(args[7]).name)

				destLane = op(destClip.parent().path)
				destName = destClip.name

				#print(sourceClip)
				#print(destClip)
				
				noClip = sourceLane.op('clip1001')

				destClip.destroy()
				destLane.copy(sourceClip, name = destName)
				
				#from 

				if op(op.LM.fetch('KEYS'))['ctrl', 1] != '1':

					sourceClip.destroy()
					sourceLane.copy(noClip, name = sourceName)

		elif mediaType in self.audioTypes:
			
			name = args[6]
			path = args[0]	
			
			self.LoadAudio(name, path,mediaType,bank,channel,clip)
			
		elif mediaType == '':
			RootFolder = args[0]
			rootFolder = self.DropFolderComp.op('rootFolder')
			rootFolder.par.rootfolder = RootFolder
			rootFolder.par.refresh.pulse()
			self.DropFolderComp.op('dropFolder').run(bank, channel, clip, mediaType, delayFrames = 1)


		if mediaType != '':
			
			selectUI = clipUI.op('select')
			if selectUI.panel.state.val == 1:

				run("args[0].click()", selectUI, delayFrames = 15)	


			curTrigClip = clipUI.fetch('CurTrigClip')
			if curTrigClip[0] == clipUI.digits:
				clipUI.Stop(op.NO_CLIP.path, clipUI.parent(), clipUI.parent().digits)

	def LoadProc(self, *args):

		data = {}	

		data['name'] = TF.SetToType(args[0])
		data['path'] = TF.SetToType(args[1])
		data['mediaType'] = TF.SetToType(args[2])
		data['bank'] = TF.SetToType(args[3])
		data['channel'] = TF.SetToType(args[4])
		data['clip'] = TF.SetToType(args [5])
		data['dataClipPath'] = TF.SetToType(args[6])
		data['compAttr'] = TF.SetToType(args[7])
		data['compPar'] = TF.SetToType(args[8])


		className = 'SetData'		
		functionName = 'RemoteLoadClip' 	
		functionPath = op.LM.path +'::'+ className +'::'+ functionName

		args = pickle.dumps([data])
		n = 64000
		args = [args[i:i + n] for i in range(0, len(args), n)]

		self.UDT_Out.send('CMD_START::' + functionPath, terminator = '')

		i = 0
		for arg in args:

			self.UDT_Out.sendBytes(arg)
			i += 1

		self.UDT_Out.send('CMD_END::None')

	def LoadComp(self, *args, local = True):

		if local:
			name = args[0]
			path = args[1] #+'/'+ args[0]
			mediaType = args[2]
			bank = args[3]
			lane = args[4]
			clip = args[5]

		else:
			name = args[0]['name']
			path = args[0]['path']
			mediaType = args[0]['mediaType']
			bank = args[0]['bank']
			lane = args[0]['channel']
			clip = args[0]['clip']


		#print(args)

		dataClipPath = me.fetch('CLIP_DATA') +'/'+ bank +'/'+ lane +'/'+ clip
		thumbSelectPath = dataClipPath +'/config/thumb'
		labelPath =dataClipPath +'/label'

		if me.fetch('NODE') == 'master':

			self.LoadProc(name, path, mediaType, bank, lane, clip, dataClipPath, '', '')
			pass

		clipComp = op(dataClipPath)

		if clipComp:

			clipCompNodeX = clipComp.nodeX
			clipCompNodeY = clipComp.nodeY
			clipComp.destroy()

		else:

			clipCompNodeX = int(clip.replace('clip', '')) * 300
			clipCompNodeY = -200

		gens = op.GENS
		pluginName = path.split('/')[-1:][0].replace('.lmGEN.tox', '')

		if pluginName != 'noClip':

			clipCompParent = op(me.fetch('CLIP_DATA') +'/'+ bank +'/'+ lane)
			clipComp = clipCompParent.loadTox(path)

			clipComp.name = clip
			clipComp.nodeX = clipCompNodeX
			clipComp.nodeY = clipCompNodeY

			plugin = clipComp.op('plugin')

			plugin.cook(force = True)
			compAttr = plugin.fetch('CompAttr')

			if not clipComp.op('label'):

				clipComp.copy(op.NO_CLIP.op('label'))

			label = clipComp.op('label')
			label.lock = False
			label.par.text = compAttr['attr']['name']
			label.lock = True


			ctrls = clipComp.op('controls')
			parNames = [r[0].val for r in plugin.op('parameters').rows()[1:]]
			compAttr['attr']['uiPath'] = ctrls

			if ctrls:
				ctrls.Createcompui(reCreate = False)

			op('/Luminosity/master/ui/clipControls/clipControls/selectControls').cook(force = True)
			
			if plugin.HasPresets:

				presets = plugin.op('presets')
				presets.initializeExtensions()
				presetControls = clipComp.op('presetControls')
				compAttr['attr']['presetControls'] = presetControls
				presetControls = compAttr['attr']['presetControls']
				presetControls.Presets = presets
				
				

			btnCtrlMapSets = ctrls.findChildren(name = 'buttonCtrlMapSet')
			for btn in btnCtrlMapSets:
				btn.op('setup').run()
			

		else:

			clipCompParent = op(me.fetch('CLIP_DATA') +'/'+ bank +'/'+ lane)
			clipComp = clipCompParent.copy(op.NO_CLIP)

			clipComp.name = clip
			clipComp.nodeX = clipCompNodeX
			clipComp.nodeY = clipCompNodeY
			clipComp.par.opshortcut = ''

			clipComp.op('controls').destroy()
			clipComp.op('presetControls').destroy()

	def LoadMovie(self, *args, local = True):

		srcPlugin = op(me.fetch('PLUGINS') + '/players/singleMoviePlayer/plugin')

		if local:
			name = args[0]
			path = args[1]
			mediaType = args[2]
			bank = args[3]
			channel = args[4]
			clip = args [5]
		
			isCropped = 0
			cropPath = ''

			movInfo = self.LoadMovieComp.op('movInfo')
			sampleRate = movInfo['sample_rate'].eval()
			rateRatio = op.LM.time.rate / sampleRate

			if movInfo['true_length']:
				#length = movInfo['true_length'].eval()
				#end = length + 1
				trueLength = movInfo['true_length'].eval()
				length = trueLength * rateRatio
				end = length 
			else:
				trueLength = 1
				length = 1
				end = 1
				
			resX = movInfo['file_resx'].eval()
			resY = movInfo['file_resy'].eval()
			audio = movInfo['mv_has_audio'].eval()


		else:
			name = args[0]['name']
			path = args[0]['path']
			mediaType = args[0]['mediaType']
			bank = args[0]['bank']
			channel = args[0]['channel']
			clip = args[0]['clip']	

			allAttr = args[0]['compAttr']
			attr = allAttr['attr']
			uiAttr = allAttr['uiAttr']
			par = args[0]['compPar']

			trueLength = attr['trueLength']
			audio = attr['audio']
			sampleRate = attr['sampleRate']
			resX = attr['resolution1']
			resY = attr['resolution2']
			end = uiAttr['TEnd']['default']

		dataClipPath = me.fetch('CLIP_DATA') +'/'+ bank +'/'+ channel +'/'+ clip
		clipComp = op(dataClipPath)


		'''
		#print('internalLoadClip:\n\t', args)
		#check for master cropped clip load:
		if re.match('master_*', name) or re.match('node*_*', name):
			#print('\t', 'IsCropped')


			node = me.fetch('NODE')
			name = name.replace('master_', node +'_', 1)
			name = re.sub('node\d', node, name, 1)
			#print('\t', name)
			pathS = path.split('/')
			pathFileName = pathS[-1:][0].replace('master_', node +'_', 1)
			pathFileName = re.sub('node\d', node, pathFileName, 1)
			print('\t', pathFileName)
			pathN = path.replace(pathS[-1:][0], pathFileName)		
			#print('\t', pathN)
			path = pathN

			isCropped = 1
			cropPath = path.replace('/'+ pathFileName, '')

			labelOP = dataClipPath +'/label')
			labelOP.lock = False
			labelOP.par.text = name
			labelOP.cook(force = True)
			labelOP.lock = True
		'''


		if clipComp.op('plugin'):
			clipComp.op('plugin').destroy()
		clipComp.copy(srcPlugin)

		pluginComp = clipComp.op('plugin')

		compAttr = pluginComp.storage['CompAttr']

		compAttr['attr']['type'] = 'movie'
		compAttr['attr']['name'] = name 
		compAttr['attr']['fileType'] = mediaType
		compAttr['attr']['trueLength'] = trueLength
		compAttr['attr']['audio'] = int(audio)
		compAttr['attr']['sampleRate'] = sampleRate
		compAttr['attr']['resolution1'] = resX
		compAttr['attr']['resolution2'] = resY
		compAttr['attr']['loadRate'] = op.LM.time.rate


		compAttr['uiAttr']['file']['default'] = path
		compAttr['uiAttr']['TStart']['rangeHigh'] = end
		compAttr['uiAttr']['TEnd']['rangeHigh'] = end
		compAttr['uiAttr']['TEnd']['default'] = end
		compAttr['uiAttr']['scrub']['rangeHigh'] = end
		compAttr['uiAttr']['scrub']['default'] = 1
		compAttr['uiAttr']['speed']['default'] = 1


		compPar = pluginComp.storage['CompPar']

		compPar['values']['file']['value'] = path

		compPar['values']['TStart']['value'] = 1
		compPar['values']['TEnd']['value'] = end
		compPar['values']['speed']['value'] = 1

		parTable = clipComp.op('plugin/parameters')

		parTable['file','value'] = path
		parTable['TStart','value'] = 1
		parTable['TEnd','value'] = end
		parTable['speed','value'] = 1
		parTable['play','value'] = 0

		if me.fetch('NODE') == 'master':
			self.LoadProc(	name, path, mediaType, 
							bank, channel, clip, dataClipPath, 
							{'attr': compAttr['attr'], 'uiAttr': compAttr['uiAttr']}, 
							compPar['values'])

		movie = clipComp.op('plugin/moviein')
		movie.par.prereadframes = me.fetch('MOVIE_PREREAD')

		if me.fetch('MOVIE_MODE') == 1 and op.DATABASE.fetch('PREVIEW_ON') == 1 and bank == me.fetch('CUR_BANK'):
			
			#print('Pre Loading Frames')
			#print('\tPreload ', dataClipPath)
			movie.preload(0)


		'''
		clipData = op(me.fetch('CLIP_DATA'))
		clipDataBase = clipData.fetch('CLIP_DATABASE', {})
		clipD =  {'type': 'movie', 'name': name, 'path': path, 'dataClipPath': dataClipPath,
		'originalPath': path, 'resX': resX, 'resY': resY, 'audio': audio, 'sampleRate': sampleRate, 'cropped': isCropped, 'cropPath': cropPath}

		clipDataBase[bank +'/'+ channel +'/'+ clip] = clipD
		clipData.store('CLIP_DATABASE', clipDataBase)
		'''

	def LoadAudio(self, *args, local = True):

		#args(path,name,mediaType,bank,channel,clip)
		#print('Loading Movie')

		name = args[0]
		path = args[1]
		mediaType = args[2]
		bank = args[3]
		channel = args[4]
		clip = args [5]

		srcPlugin = op(me.fetch('PLUGINS') + '/players/audioPlayer/plugin')
		dataClipPath = me.fetch('CLIP_DATA') +'/'+ bank +'/'+ channel +'/'+ clip
		clipComp = op(dataClipPath)


		audioInfo = self.LoadAudioComp.op('audioInfo')
		sampleRate = audioInfo['sample_rate'].eval()
		length = audioInfo['true_file_length_frames'].eval()
		end = length + 1

		if clipComp.op('plugin'):
			clipComp.op('plugin').destroy()
		clipComp.copy(srcPlugin)

		pluginComp = clipComp.op('plugin')
		compAttr = pluginComp.storage['CompAttr']

		compAttr['attr']['type'] = 'audio'
		compAttr['attr']['name'] = name 
		compAttr['attr']['fileType'] = mediaType
		compAttr['attr']['length'] = length

		compAttr['uiAttr']['file']['default'] = path
		compAttr['uiAttr']['sampleRate']['default'] = sampleRate
		compAttr['uiAttr']['trimStart']['rangeHigh'] = end
		compAttr['uiAttr']['trimEnd']['rangeHigh'] = end
		compAttr['uiAttr']['trimEnd']['default'] = end
		compAttr['uiAttr']['scrub']['rangeHigh'] = end
		compAttr['uiAttr']['scrub']['default'] = 1
		compAttr['uiAttr']['speed']['default'] = 1


		compPar = pluginComp.storage['CompPar']

		compPar['values']['file']['value'] = path
		compPar['values']['sampleRate']['value'] = sampleRate
		compPar['values']['trimStart']['value'] = 1
		compPar['values']['trimEnd']['value'] = end
		compPar['values']['scrub']['value'] = 1
		compPar['values']['speed']['value'] = 1

		if me.fetch('NODE') == 'master':
			self.LoadProc(name, path, mediaType, bank, channel, clip, dataClipPath, [compAttr['attr'], compAttr['uiAttr']], compPar['values'])

		parTable = pluginComp.op('parameters')

		parTable['file','value'] = path
		parTable['sampleRate','value'] = sampleRate
		parTable['trimStart','value'] = 1
		parTable['trimEnd','value'] = end
		parTable['speed','value'] = 1
		parTable['play','value'] = 0

		audioPlayer = pluginComp.op('audiofilein')
		audioPlayer.par.file = path

		setDefault = "op('loadAudio/loader').par.file = 'C:/Program Files/Derivative/TouchDesigner088/Samples/Audio/JeremyCaulfield_www.dumb-unit.com.mp3'"

		run(setDefault, delayFrames = 10)

	def RemoteLoadClip(self, data):

		if data['mediaType'] in self.movTypes:

			self.LoadMovie(data, local = False)

		elif data['mediaType'] in self.audioTypes:

			self.LoadAudio(data, local = False)

		elif data['mediaType'] == 'COMP':

			self.LoadComp(data, local = False)

		print(data['mediaType'])



					



