def plot_hist(bin_size,bin_list, upper =None):
	import matplotlib.pyplot as plt
	for bins in bin_list:
		fig = plt.figure()
		ax = fig.add_subplot(1,1,1)
		up_bound = upper or max(bins)
		x = [i for i in range(up_bound+1)]
		y = [bins[i] for i in range(up_bound+1)]
#		print x
#		print y
		ax.bar(x,y,width=1)
		plt.show()

