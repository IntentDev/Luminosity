numItems = me.fetch('NumItems')
loadList = me.fetch('LoadList')
curId = me.fetch('CurId', 0)
bankOverride = args[0]


if curId < numItems:
	name = loadList[curId][0]
	path = loadList[curId][1]
	mediaType = loadList[curId][2]
	bank = loadList[curId][3]
	channel = loadList[curId][4]
	clip = loadList[curId][5]
	
	
	print('MultiLoad', loadList[curId][0])
	#print('multiLoad ', name)
	#n2 = name.split('.')
	
	#name = '.'.join(n2[:-1])
	#print(name)

	if curId == 0:
		clipId = int(clip.replace('clip', '')) + curId
		channelId = int(channel.replace('clipLane', ''))
		bankId = int(bank.replace('bank', ''))
		prevBank = bank

		me.store('ClipId', clipId)
		me.store('ChannelId', channelId)
		me.store('BankId', bankId)
		#me.store('RootMovieMode', me.fetch('MOVIE_MODE'))
		#me.fetch('ROOT').store('MOVIE_MODE', 0)
		realTime(0)

	else:
		clipId = me.fetch('ClipId') + 1
		channelId = me.fetch('ChannelId')
		bankId = me.fetch('BankId')	
		prevBank = me.fetch('PrevBank')
		
	numScenes = op.DATABASE.fetch('NUM_CLIP_SCENES')
	numChans = op.DATABASE.fetch('NUM_CLIP_LANES')
	numBanks = op.DATABASE.fetch('NUM_CLIP_BANKS')

	if bankOverride == 1 and prevBank != bank:
		clipId = 0
		channelId = 0
		me.store('ChannelId', channelId)

	if clipId >= numScenes:
		clipId = 0
		channelId += 1
		me.store('ChannelId', channelId)
		
	if channelId >= numChans:
		clipId = 0
		channelId = 0
		bankId += 1
		me.store('ChannelId', channelId)
		me.store('BankId', bankId)
		
	if bankId >= numBanks:
		curId = numItems

	me.store('ClipId', clipId)

	clip = 'clip' + str(clipId)
	channel = 'clipLane' + str(channelId)
	if bankOverride == 0:
		bank = 'bank' + str(bankId)

	#print(clip, channel, bank, name)
	bankId = int(bank.replace('bank', ''))
	
	if curId < numItems and bankId < op.DATABASE.fetch('NUM_CLIP_BANKS'):
		op('makeThumb').run(name, path, mediaType, bank, channel, clip)

	me.store('CurId', curId + 1)
	me.store('PrevBank', bank)
	me.run(bankOverride, delayFrames = 2)
	
	
	clipUI = op.CLIP_LANES_UI.op(channel).op(clip)
	curTrigClip = clipUI.fetch('CurTrigClip')
	if curTrigClip[0] == clipUI.digits:
		clipUI.Stop(op.NO_CLIP.path, clipUI.parent(), clipUI.parent().digits)
	

else:
	#me.fetch('ROOT').store('MOVIE_MODE', me.fetch('RootMovieMode'))
	me.store('LoadList', [])
	me.store('NumItems', 0)
	me.store('CurId', 0)
	realTime(1)
	
	mod.extPFMClips.ClearClipControlsFindClip()
	#run("mod.extPFMClips.ClearClipControls()", delayFrames = 15, fromOP = me)