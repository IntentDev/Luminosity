class Presets(object):

	def __init__(self, controls):

		self.controls = op(controls)

	def StoreControls(self, preset):

		import copy

		presetName = str(preset)

		storeComp = self.controls.fetch('StoreComp')
		#print('Stored   ' + presetName)

		compPar = copy.deepcopy(storeComp.fetch('CompPar'))

		compPresets = storeComp.fetch('CompPresets')

		compPresets['presets'][presetName] = compPar

	def RecallControls(self, preset, setPar = True):

		import copy

		#presetName = 'preset4'
		presetName = str(preset)

		parDest = op(self.controls.fetch('Parameters'))
		storeComp = self.controls.fetch('StoreComp')

		compPresets = storeComp.fetch('CompPresets')

		if presetName in compPresets['presets']:

			compPar = copy.deepcopy(compPresets['presets'][presetName])

			op(storeComp).store('CompPar', compPar)

			preset = compPar['values']

			for gadget in preset.items():
				
				#print(gadget[0], gadget[1])
				
				if self.controls.op(gadget[0]):

					self.controls.op(gadget[0]).op('setUI').run(gadget[1])
	
					for par in gadget[1].items():
						if isinstance(par[1], int) or isinstance(par[1], float) or isinstance(par[1], str):
							parDest[gadget[0],par[0]] = par[1]
				