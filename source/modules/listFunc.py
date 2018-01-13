import kMath

mathK = kMath.Math()

def GetCellList(input):

	from ast import literal_eval
	import td
	
	outputList = []
	
	if isinstance(input, td.Cell):
		input = input.val
	
	if not input:	
		return outputList
		
	if input[0] == '[' and input[-1:] == ']':

		input = input.strip('[')
		input = input.strip(']')
		
	else:
		listFormat = False
		
	items = input.split(',')
	
	for item in items:

		item = item.strip()
		item = item.strip("'")
		item = item.strip("'")
		item = item.strip('"')
		item = item.strip('"')
		
		try:
			if isinstance(literal_eval(item), float):
				item = float(item)
				
			elif isinstance(literal_eval(item), int):
				item = int(item)
		except:
			pass
			
		outputList.append(item)
	
	return outputList

def MListFillMatrix(mList):
	
	matrix = tdu.Matrix()

	for i in range(0, 16):

		n = i % 4
		m = mathK.StepVal(16, 4, i)
		matrix[n, m] = mList[i]
	
	return matrix

def MListFillTable(mList, table):

	i = 0

	for r in range(0, 4):
		
		for c in range(0, 4):
		
			table[c, r] = mList[i]
			i += 1
			
def MatrixFillList(matrix):

	mList = []
	
	for r in range(0, 4):
		
		for c in range(0, 4):
		
			mList.append(matrix[c, r])
	
	return mList

def MatrixFillTable(matrix, table):

	for i in range(0, 16):

		n = i % 4
		m = mathK.StepVal(16, 4, i)
		table[n, m] = matrix[n, m]
	

