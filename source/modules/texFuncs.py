def Fit(inTexDim, texLimit):

	if inTexDim[0] > inTexDim[1]:
		a = texLimit[0] / inTexDim[0]
	else:
		a = texLimit[1] / inTexDim[1]
		
	w = a * inTexDim[0]
	h = a * inTexDim[1]
	
	return [w, h]
	 
	 
