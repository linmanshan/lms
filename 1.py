import commands
a=0
while 1:
	user=raw_input('This is a Tone Analyzer. Please enter the text you want:\n')
	b=str(a)
	if a == 0:
		print commands.getoutput("curl -XGET --header \'Content-Type:application/json\' -d \'{\"text\":\""+user+"\",\"id\":"+b+"}\' \'127.0.0.1:5000\'")
	else:
		print commands.getoutput("curl -XGET --header \'Content-Type:application/json\' -d \'{\"text\":\""+user+"\",\"id\":"+b+"}\' \'127.0.0.1:5000/trans?\'")
	a = a + 1
