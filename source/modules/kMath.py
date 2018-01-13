class MatMath(object):

	def __init__(self):
		pass

		
	def CalcProjM(	self, fov, resX, resY, near, far, 
					cropLeft, cropRight, 
					cropBottom, cropTop):
		
###		calculate projection matrix with cropping
###		returns a list with the matrix, the matrix, render width,
###		and the render height in list form 

		mathK = Math()
		
		fov = math.radians(fov)
		aspect = resX / resY
		
		renderWidth = cropRight - cropLeft
		renderHeight = cropTop - cropBottom
		
		tileRatioX = resX / renderWidth
		tileRatioY = resY / renderHeight
						
		tileOffsetX = mathK.RangeVal(0, resX, -tileRatioX, tileRatioX, cropLeft, 'float') + 1
		tileOffsetY = mathK.RangeVal(0, resY, -tileRatioY, tileRatioY, cropBottom, 'float') + 1
		
		zoomX = 1 / (math.tan(fov / 2)) * tileRatioX
		zoomY = (1 / (math.tan(fov / 2))) * aspect * tileRatioY
		clipFar = -(far + near) / (far - near)
		clipNear = (-2 * near * far) / (far - near)
	
		projM = tdu.Matrix()
		projMList =	[zoomX, 0, 0, 0, 
					0, zoomY, 0, 0, 
					tileOffsetX, tileOffsetY, clipFar, -1, 
					0, 0, clipNear, 0]
		
		for i in range(0, 16):
		
			n = i % 4
			m = mathK.StepVal(16, 4, i)
			projM[n, m] = projMList[i]

		return [projM, projMList, renderWidth, renderHeight]
	

	
	def CalcOrthoProjM(	self, wWidth, resX, resY, near, far, 
						cropLeft, cropRight, 
						cropBottom, cropTop):

		mathK = Math()

		aspect = resY / resX
		wHeight = wWidth * aspect
		renderWidth = cropRight - cropLeft
		renderHeight = cropTop - cropBottom
		tileRatioX = resX / renderWidth
		tileRatioY = resY / renderHeight				
		tileOffsetX = -(mathK.RangeVal(0, resX, -tileRatioX, tileRatioX, cropLeft, 'float') + 1)
		tileOffsetY = -(mathK.RangeVal(0, resY, -tileRatioY, tileRatioY, cropBottom, 'float') + 1)

		l = mathK.RangeVal(0, resX, 0, wWidth, cropLeft, 'float')
		r = mathK.RangeVal(0, resX, 0, wWidth, cropRight, 'float')
		b = mathK.RangeVal(0, resY, 0, wHeight, cropBottom, 'float')
		t = mathK.RangeVal(0, resY, 0, wHeight,  cropTop, 'float')

		x = 2 / (r - l)
		y = 2 / (t - b) 
		f = -2 / (far - near)
		n = -(far + near) / (far - near)

		projM = tdu.Matrix()
		projMList =	[x, 0, 0, 0, 
					0, y, 0, 0, 
					0, 0, f, 0, 
					tileOffsetX, tileOffsetY, n, 1]

		for i in range(0, 16):

			n = i % 4
			m = mathK.StepVal(16, 4, i)
			projM[n, m] = projMList[i]

		return [projM, projMList, renderWidth, renderHeight]
		
		
		
class Math(object):

	def __init__(self):
		pass

			
	def StepVal(self, range, stepSize, value):
	
		val = math.floor(value / range * stepSize)
		
		return val		

		
	def ExpandVal(self, low, high, value, format):

		value = ((high - low) * (value)) / 1 + low

		if format == 'integer':
			value = round(value)

		return value


	def NormalizeVal(self, low, high, value):

		return (value - low) / (high - low)


	def RangeVal(self, oLow, oHigh, nLow, nHigh, value, format):

		value = ((nHigh - nLow) * (value -oLow)) / (oHigh - oLow)  + nLow

		if format == 'integer':
			value = round(value)

		return value	
		
		
