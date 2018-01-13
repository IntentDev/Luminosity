CropData = {}
dat = op('cropData')
	
from tableFunc import SetToType as sType

cData = {r[0].val:sType(r[1].val) for r in dat.rows()}

if (me.fetch('NODE') == 'master' or op.DATABASE.fetch('PREVIEW_ON') == 1)  and op.DATABASE.fetch('PREVIEW_RES_MODE') != 2:
	camData = op.DATABASE.fetch('FULL_MAP_CAM_DATA')
	resMode = op.DATABASE.fetch('PREVIEW_RES_MODE')

	numOutputs = [cData['numOutputs'], 1][resMode]
	resX = [camData['resX'], 1920][resMode]
	resY = [camData['resY'], 1920 * (camData['resY'] / camData['resX'])][resMode]
	fov = camData['camFOV']
	orthoWidth = camData['camOrthoWidth']
	near = camData['camNearClip']
	far = camData['camFarClip']
	cropLeft = 0
	cropRight = resX
	cropBottom =0
	cropTop = resY
	
	import kMath
	mtrx = kMath.MatMath()
	
	projML = mtrx.CalcProjM(	fov, resX, resY, near, far, 
								cropLeft, cropRight, 
								cropBottom, cropTop)

	orthoProjML = mtrx.CalcOrthoProjM(	orthoWidth, resX, resY, near, far, 
										cropLeft, cropRight, 
										cropBottom, cropTop)
	

	projM = projML[0]
	projL = projML[1]
	orthoProjM = orthoProjML[0]
	orthoProjL = orthoProjML[1]
	renderWidth = projML[2]
	renderHeight = projML[3]
	
	#print(orthoProjL)
	
	cData['numOutputs'] = numOutputs
	cData['cropMatrix'] = projL
	cData['cropOrthoMatrix'] = orthoProjL
	cData['cropDim'] = [resX, resY]
	cData['cropLeft'] = cropLeft
	cData['cropRight'] = cropRight
	cData['cropBottom'] = cropBottom
	cData['cropTop'] = cropTop

	#print('Storing Full Map Crop Data')


	op.DATABASE.store('FULL_MAP_CROP_DATA', cData)

else:
	camData = op.DATABASE.fetch('FULL_MAP_CAM_DATA')
	resMode = op.DATABASE.fetch('PREVIEW_RES_MODE')

	numOutputs = [cData['numOutputs'], 1]
	resX = cData['cropDim'][0]
	resY = cData['cropDim'][1]
	fov = camData['camFOV']
	orthoWidth = camData['camOrthoWidth']
	near = camData['camNearClip']
	far = camData['camFarClip']
	cropLeft = cData['cropLeft']
	cropRight = cData['cropRight']
	cropBottom = cData['cropBottom']
	cropTop = cData['cropTop']
	
	import kMath
	mtrx = kMath.MatMath()
	
	projML = mtrx.CalcProjM(	fov, resX, resY, near, far, 
								cropLeft, cropRight, 
								cropBottom, cropTop)

	orthoProjML = mtrx.CalcOrthoProjM(	orthoWidth, resX, resY, near, far, 
										cropLeft, cropRight, 
										cropBottom, cropTop)
	

	projM = projML[0]
	projL = projML[1]
	orthoProjM = orthoProjML[0]
	orthoProjL = orthoProjML[1]
	renderWidth = projML[2]
	renderHeight = projML[3]
	
	#print(orthoProjL)
	
	cData['numOutputs'] = numOutputs
	cData['cropMatrix'] = projL
	cData['cropOrthoMatrix'] = orthoProjL
	cData['cropDim'] = [resX, resY]
	cData['cropLeft'] = cropLeft
	cData['cropRight'] = cropRight
	cData['cropBottom'] = cropBottom
	cData['cropTop'] = cropTop

	#print('Storing Full Map Crop Data')


	op.DATABASE.store('FULL_MAP_CROP_DATA', cData)	