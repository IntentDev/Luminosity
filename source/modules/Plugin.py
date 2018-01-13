
class Plugin(object):

	def __init__(self, ownerComp):
		# The component to which this extension is attached

		self.ownerComp = ownerComp
		self.CompAttr = ownerComp.fetch('CompAttr')
		self.CompPar = ownerComp.fetch('CompPar')
		self.UIAttr = self.CompAttr['uiAttr']
		self.Attr = self.CompAttr['attr']
		self.Type = self.Attr['type']

		if self.ownerComp.op('config'):
			self.Config = self.ownerComp.op('config')
			self.ParexecCallbacks = self.Config.op('parexecCallbacks')
		else:
			self.ParexecCallbacks = self.ownerComp.op('parexecCallbacks')

		self.Parameters = self.ownerComp.op('parameters')

		self.HasPresets = False
		self.HasModRouter = False
		self.HasAnimation = False

		if self.HasAnimation:
			self.Animation = self.ownerComp.op('animation')
			self.Animation0 = self.Animation.op('animation0')
			self.Animation1 = self.Animation.op('animation1')

		#used if triggerd by cue and cue is recalling a preset
		self.CuePreset = False

		#self.Presets = self.ownerComp.op('presets')
	
	#################
	# parCallbacks

	def Pluginactive(self, *args):
		self.Active = args[0].eval()

	def Animactive(self, *args):
		self.AnimActive = args[0].eval()


	#################
	# properties

	@property
	def Active(self):
		return self.ownerComp.par.Pluginactive.eval()

	@Active.setter
	def Active(self, value):
		#print('Active')
		self.ParexecCallbacks.par.active = False
		self.ownerComp.par.Pluginactive = value

		if self.HasModRouter:
			self.ownerComp.op('modRouter/active').par.index = value

		if self.HasAnimation and self.AnimActive:
			self.Animation0.allowCooking = value
			self.Animation1.allowCooking = value

			if value and self.CuePreset == False:
				
				self.Animation.CuePlayAnim()

			else:
				self.CuePreset = False
			

		run("args[0].par.active = True", self.ParexecCallbacks, delayFrames = 1, fromOP = self.ParexecCallbacks)


	@property
	def AnimActive(self):
		if self.HasAnimation:
			return self.ownerComp.par.Animactive.eval()
		else: 
			return False

	@AnimActive.setter
	def AnimActive(self, value):
		self.ownerComp.par.Animactive = value

		if self.HasAnimation:
			#self.Animation.op('switchAnimActive').par.index = value
			
			if self.HasPresets:
				self.ownerComp.op('presets').AnimActive = value

			if self.Active:
				self.Animation0.allowCooking = value
				self.Animation1.allowCooking = value


