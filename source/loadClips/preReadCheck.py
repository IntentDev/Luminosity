movLoader = op('movieLoad')

if movLoader.isFullyPreRead == True:

	
	op(args[6]).lock = False
	op(args[7]).lock = False
	op('lock').run(args[0],args[1],args[2],args[3],args[4],args[5],args[6], args[7], delayFrames = 1)

else:

	me.run(args[0],args[1],args[2],args[3],args[4],args[5],args[6], args[7], delayFrames = 1)
	print('preReading')