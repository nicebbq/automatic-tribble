import time

def example(seconds):
	print('init')
	for i in range(seconds):
		print(i)
		time.sleep(1)
	print('done')

