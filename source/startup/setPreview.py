sSettings = op(me.fetch('SERVER_DATA')).fetch('Settings')
node = me.fetch('NODE')
previewNode = sSettings['previewNode']
previewOn = [0,1][int(previewNode == node)]
previewResMode = sSettings['previewResMode']

ROOT = me.fetch('ROOT')
op.DATABASE.store('PREVIEW_NODE', previewNode)
op.DATABASE.store('PREVIEW_ON', previewOn)
op.DATABASE.store('PREVIEW_RES_MODE', previewResMode)



if node != 'master':
	
	dOuts = op(me.fetch('TO_NODES')).findChildren(type = touchoutDAT)
	cOuts = op(me.fetch('TO_NODES')).findChildren(type = touchoutCHOP)
	
	for o in dOuts:
		print(o)
		o.destroy()
	for o in cOuts:
		print(o)
		o.destroy()
		
	op(me.fetch('MASTER')).allowCooking = False
	op(me.fetch('PROC')).allowCooking = True
	ROOT.store('MASTER_MODE', 0)
	ROOT.store('MASTER_MODE_INV', 1)
	
	op(me.fetch('CLIP_DATA') + '/preload').run(me.fetch('CUR_BANK'))
	
else:
	op(me.fetch('MASTER')).allowCooking = True	
	if previewOn == 1:
		op(me.fetch('PROC')).allowCooking = True	
		op(me.fetch('CLIP_DATA') + '/preload').run(me.fetch('CUR_BANK'))
	else:
		op(me.fetch('PROC')).allowCooking = False
	
	ROOT.store('MASTER_MODE', 1)
	ROOT.store('MASTER_MODE_INV', 0)	
	
	
#op(me.fetch('COMMAND_PROCESSOR')).cook(force = True, recurse = True)

