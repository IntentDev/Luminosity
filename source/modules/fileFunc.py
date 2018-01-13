def rawStr(string):
	rStr = "%r"%string
	return rStr[1:-1]

def GetRelPath(absPath):

	projPath = project.folder.split('/')

	if '/' in absPath:
		absPathL = absPath.split('/')
	elif '//' in absPath:
		absPathL = absPath.split('\\')

	if projPath[0] == absPathL[0]:

		pFIndex = len(projPath) - 1
		projFolder = projPath[pFIndex]
		dIndex = -1

		for i in projPath:
			if i in absPathL:
				absPathL.remove(i)
				dIndex += 1

		indexDif = pFIndex - dIndex

		if indexDif <= 2:
			pre = [[], ['..'], ['..', '..']][max(0, indexDif)]
			absPathL = pre + absPathL
			relPath = '/'.join(absPathL)
			return(relPath)
		else:
			return(absPath)
	else:
		return(absPath)