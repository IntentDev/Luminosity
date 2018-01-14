paths = op('paths')
loadMethod = ui.messageBox('Load Folder Method', 'Load Media from Folders by:', buttons = ['Folder per Bank', 'Fill All Clips'])

bank = args[0]
channel = args[1]
clip = args[2]
mediaType = args[3]
loadList = []
fullCount = 0
bankOverride = 0

if loadMethod == 0:

	bankId = int(bank.replace('bank', ''))
	folder = paths[1,0].val
	count = 0
	bankOverride = 1

	numScenes = op.DATABASE.fetch('NUM_CLIP_SCENES')
	numLanes = op.DATABASE.fetch('NUM_CLIP_LANES')
	numClips = numScenes * numLanes

	for r in paths.rows()[1:]:
		if folder != r[0].val:
			bankId += 1
			count = 0

		bank = 'bank' + str(bankId)
		name = r[1].val
		path = r[2].val
		n2 = name.split('.')
		name = '.'.join(n2[:-1])
		mediaType = path.split('.')[-1:][0]

		if count < numClips:
			loadList.append([name, path, mediaType, bank, channel, clip])
			fullCount += 1
		folder = r[0].val	
		count += 1

elif loadMethod == 1:

	for r in paths.rows()[1:]:
		name = r[1].val
		n2 = name.split('.')
		name = '.'.join(n2[:-1])
		path = r[2].val
		mediaType = path.split('.')[-1:][0]
		loadList.append([name, path, mediaType, bank, channel, clip])

	fullCount = paths.numRows - 1

multiLoad = op('../loadMovie/multiLoad')
multiLoad.store('LoadList', loadList)
multiLoad.store('NumItems', fullCount)
multiLoad.store('CurId', 0)
multiLoad.run(bankOverride, delayFrames = 1)





