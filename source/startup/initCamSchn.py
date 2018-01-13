cA = '''
cSchn = op(op('/Luminosity').fetch('CAMSCHNAPPR'))
cSchn.op('activate').run(0)
'''
cSchn = op(me.fetch('CAMSCHNAPPR'))
cSchn.op('activate').run(1)
cSchn.cook(force = True, recurse = True)
run(cA, delayFrames = 5)