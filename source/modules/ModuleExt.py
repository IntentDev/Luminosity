"""
Extension classes enhance TouchDesigner component networks with python
functionality. An extension can be accessed via ext.ExtensionClassName from
any operator within the extended component. If the extension is "promoted", all
its attributes with capitalized names can be accessed directly through the
extended component, e.g. op('yourComp').ExtensionMethod()
"""

class ModuleExt:
	"""
	ModuleExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	def GetModuleNames(self):

		self.ModuleNames = [module.name for module in self.ownerComp.findChildren(type = textDAT)]
		self.ModuleNames.sort()

	def Editmodules(self, *args):

		self.GetModuleNames()

		for mName in self.ModuleNames:

			i = self.ModuleNames.index(mName)
			op.LM.Delay(delayFrames = i, fromOP = me).Call(op(mName).par.edit, 'pulse')






