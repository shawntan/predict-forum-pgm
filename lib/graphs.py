import os
def plot_hist(bin_size, bin_list, directory=None, upper=None):
	if not os.path.exists(directory): os.makedirs(directory)
	import matplotlib.pyplot as plt
	count = 1
	for bins in bin_list:
		fig = plt.figure()
		ax = fig.add_subplot(1,1,1)
		up_bound = upper or max(bins)
		x = [i for i in range(up_bound+1)]
		y = [bins[i] for i in range(up_bound+1)]
#		print x
#		print y
		ax.bar(x,y,width=1)
		if not directory:
			plt.show()
		else:
			plt.savefig('%s/%03d'%(directory, count))
		count += 1

