"""
Extension classes enhance TouchDesigner component networks with python
functionality. An extension can be accessed via ext.ExtensionClassName from
any operator within the extended component. If the extension is "promoted", all
its attributes with capitalized names can be accessed directly through the
extended component, e.g. op('yourComp').ExtensionMethod()
"""

class ChannelFXExt:
	"""
	ChannelFXExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def RouteFX(self, channel, val):

		routing = self.ownerComp.op('routing')
		routingLen = routing.numRows + 1
		states = self.ownerComp.op('states')
		stateLen = states.numChans

		onChans = []

		for i in range(1, routingLen):

			for n in range(i - 1, stateLen):		
				state = int(states[n])
				chan = states[n].name

				if state == 1:
					routing[i,1] = chan
					break

		for i in states.chans():

			if int(i) == 0:
				routing[i.name, 1] = 'off'
				#print(i.name)

		#op(self.ownerComp.fetch('FXSlotsPath')+'/'+ channel.name + '/plugin').allowCooking = int(val)
		op(self.ownerComp.fetch('FXSlotsPath')+'/'+ channel.name + '/plugin').Active = int(val)
		
	def RouteFXInit(self):

		routing = self.ownerComp.op('routing')
		routingLen = routing.numRows + 1
		states = self.ownerComp.op('states')
		stateLen = states.numChans

		onChans = []

		for i in range(1, routingLen):

			for n in range(i - 1, stateLen):		
				state = int(states[n])
				chan = states[n].name

				if state == 1:
					routing[i,1] = chan
					break

		for i in states.chans():

			if int(i) == 0:
				routing[i.name, 1] = 'off'
					#print(i.name)

		for i in range(6):	
			plugin = op(self.ownerComp.fetch('FXSlotsPath')+'/slot'+ str(i) + '/plugin')
			plugin.par.reinitextensions.pulse()
			plugin.ext.Plugin.Active = int(self.ownerComp.op('datto1')[i].eval()) 
