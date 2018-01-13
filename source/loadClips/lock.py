movLoader = op('movieLoad')
thumbPath = op('thumb').path
thumbSelectPath = args[6]
labelPath = args[7]

op(thumbSelectPath).lock = True
op(labelPath).lock = True

parent().LoadMovie.run(args[0],args[1],args[2],args[3],args[4],args[5],args[6])
