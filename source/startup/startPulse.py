pulseOff = "me.fetch('ROOT').store('START_PULSE', 0)"

me.fetch('ROOT').store('START_PULSE', 1)

run(pulseOff, delayFrames = 5)