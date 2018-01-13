if me.var('NODE'):
	node = me.var('NODE')
else:
	node = 'master'
if me.var('SERVER'):		
	server = int(me.var('SERVER'))
else:
	server = 0
if me.var('GPU'):	
	gpu = max(0, int(me.var('GPU')))
else:
	gpu = 0	
	
serverPath = me.fetch('SERVER_DATA') +'/server'+ str(server)
gpuPath = serverPath +'/gpu'+ str(gpu)

ROOT = me.fetch('ROOT')

ROOT.store('NODE', node)
ROOT.store('SERVER', server)
ROOT.store('GPU', gpu)
ROOT.store('SERVER_PATH', serverPath)
ROOT.store('GPU_PATH', gpuPath)

remoteMode = op.DATABASE.fetch('REMOTE_MODE')

if remoteMode == 3 and node != 'master':

	project.realTime = False

		
	

