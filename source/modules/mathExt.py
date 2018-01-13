class Math(object):

	def __init__(self, comp):

		self.comp = comp
		
	def ExpandVal(self, low, high, format, value):

		value = ((high - low) * (value)) / 1 + low

		if format == 'integer':
			value = round(value)

		return value

	def NormalizeVal(self, low, high, value):

		return (value - low) / (high - low)

	def RangeVal(self, oLow, oHigh, nLow, nHigh, format, value):

		value = ((nHigh - nLow) * (value -oLow)) / (oHigh - oLow)  + nLow

		if format == 'integer':
			value = round(value)

		return value
				