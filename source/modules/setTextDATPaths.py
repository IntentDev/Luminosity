textDATs = parent().findChildren(type = textDAT)


for dat in textDATs:

	if dat != me:
		print(dat)

		path = '../source/' + parent().name + '/' + dat.name + '.py'

		dat.save(path)

		dat.par.file = path
		dat.par.loadonstart = True
		dat.par.write = True
