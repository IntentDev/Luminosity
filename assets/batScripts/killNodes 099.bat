@echo on

cd assets\externalTools\PSTools

start pskill.exe \\192.168.0.102 -t -u XI-USER -p pool touchdesigner099.exe
start pskill.exe \\192.168.0.103 -t -u XI-USER -p pool touchdesigner099.exe
start pskill.exe \\192.168.0.104 -t -u XI-USER -p pool touchdesigner099.exe
