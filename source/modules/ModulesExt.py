class ModulesExt:
	"""
	ModulesExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.folder = ownerComp.op('folder1')

	def ReloadModule(self, row):

		name = self.folder[row, 0].val.split('.')[0]

		fileOP = self.ownerComp.op(name)

		if fileOP:

			fileOP.par.loadonstartpulse.pulse()

	def Editallmodules(self, *args):
		
		modules = [m for m in self.ownerComp.findChildren(type = textDAT)]

		for i, m in enumerate(modules):
		
			if m.name != 'ModulesExt':

				run("args[0].par.edit.pulse()", m, delayFrames = i)






