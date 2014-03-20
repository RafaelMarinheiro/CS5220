import sys
import numpy
import matplotlib.pyplot as plt

#Model time = an + bn(p-1) + yn/p

dataSrc = ["1k", "2k", "4k", "8k", "16k"]
particles = [1053, 2057, 4116, 8424, 15972]
processors = [1, 2, 3, 4, 5, 6, 7, 8]

data = []
dataPerProcessors = [numpy.array([])]*len(processors)

frames = 50

def modelFor(n, p, model):
	return (model[0]*n + model[1]*(p-1) + (model[2]*n)/p)*frames

def readData():
	for src in range(len(dataSrc)):
		temp = numpy.loadtxt("data"+ dataSrc[src]+".txt")
		temp = temp.transpose()
		data.append(temp)
		for i in range(len(processors)):
			dataPerProcessors[i] = numpy.append(dataPerProcessors[i], data[src][1][i])

def fitModel():
	a = []
	b = []
	c = []
	y = []
	for i in range(len(particles)):
		a = numpy.hstack((a, frames*particles[i]*numpy.ones(len(data[i][0]))))
		b = numpy.hstack((b, frames*(data[i][0] - numpy.ones(len(data[i][0])))))
		c = numpy.hstack((c, frames*particles[i]*(numpy.ones(len(data[i][0]))/data[i][0])))
		y = numpy.hstack((y, data[i][1]))

	A = numpy.vstack([a, b, c])
	model = numpy.linalg.lstsq(A.T, y)[0]
	print "alpha=" + str(model[0])
	print "beta=" + str(model[1])
	print "gamma=" + str(model[2])
	return model

# : $\alpha + \beta\cdot (p-1) + \frac{\gamma}{p}$"+"\n"+ r"$\alpha = " + str(a) + r"$,"+ "\n"+ r"$ \beta = " + str(b) + r"$," + "\n"+ r"$ \gamma = " + str(c) + r"$

def make_processor_plots(model):
	for i in range(len(particles)):
		plt.figure()
		plt.plot(data[i][0], data[i][1], '.', label="Measured", hold=False)
		plt.plot(data[i][0], modelFor(particles[i], data[i][0], model), '-', label=r"Model", hold=True)
		plt.xlabel('Number of Processors')
		plt.ylabel('Time (s)')
		lgd = plt.legend(bbox_to_anchor=(0.70, 0.95), loc=2, borderaxespad=0.)
		plt.savefig("plot_data"+ dataSrc[i] +'.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')

def make_global_processor_plot(model):
	plt.figure()
	plt.xlabel('Number of Processors')
	plt.ylabel('Time (s)')
	for i in range(len(particles)):
		plt.plot(data[i][0], data[i][1], '.', label="Measured: n=" + str(particles[i]), hold=True)
		plt.plot(data[i][0], modelFor(particles[i], data[i][0], model), '-', label=r"Model: n=" + str(particles[i]), hold=True)
		
	lgd = plt.legend(bbox_to_anchor=(0.53, 0.96), loc=2, borderaxespad=0.)	
	plt.savefig("plot_allData.pdf", bbox_extra_artists=(lgd,), bbox_inches='tight')

def make_particles_plots(model):
	xp = numpy.linspace(1, 16500, 100)
	for i in range(len(processors)):
		plt.figure()
		plt.plot(particles, dataPerProcessors[i], '.', label="Measured", hold=False)
		plt.plot(xp, modelFor(xp, processors[i], model), '-', label=r"Model", hold=True)
		plt.xlabel('Number of Particles')
		plt.ylabel('Time (s)')
		lgd = plt.legend(bbox_to_anchor=(0.05, 0.95), loc=2, borderaxespad=0.)
		plt.savefig("plot_core"+ str(processors[i]) +'.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')

def make_global_particle_plot(model):
	xp = numpy.linspace(1, 16500, 100)
	plt.figure()
	plt.xlabel('Number of Particles')
	plt.ylabel('Time (s)')
	for i in range(len(processors)):
		plt.plot(particles, dataPerProcessors[i], '.', label="Measured", hold=True)
		plt.plot(xp, modelFor(xp, processors[i], model), '-', label=r"Model", hold=True)
	lgd = plt.legend(bbox_to_anchor=(1.05, 1.0), loc=2, borderaxespad=0.)
	plt.savefig("plot_allCore.pdf", bbox_extra_artists=(lgd,), bbox_inches='tight')

def make_particles_plots_loglog(model):
	xp = numpy.linspace(1000, 16500, 10)
	for i in range(len(processors)):
		plt.figure()
		plt.xlim([2**9,2**14])
		plt.loglog(particles, dataPerProcessors[i], '.', label="Measured", hold=False)
		plt.loglog(xp, modelFor(xp, processors[i], model), '-', label=r"Model", hold=True)
		plt.xlabel('Number of Particles')
		plt.ylabel('Time (s)')
		lgd = plt.legend(bbox_to_anchor=(0.05, 0.95), loc=2, borderaxespad=0.)
		plt.savefig("plot_coreloglog"+ str(processors[i]) +'.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')

def make_global_particle_plot_loglog(model):
	xp = numpy.linspace(1000, 16500, 10)
	plt.figure()
	plt.xlabel('Number of Particles')
	plt.ylabel('Time (s)')
	plt.xlim([2**9,2**14])
	for i in range(len(processors)):
		plt.loglog(particles, dataPerProcessors[i], '.', label="Measured", hold=True)
		plt.loglog(xp, modelFor(xp, processors[i], model), '-', label=r"Model", hold=True)
	lgd = plt.legend(bbox_to_anchor=(1.05, 1.0), loc=2, borderaxespad=0.)
	plt.savefig("plot_allCoreloglog.pdf", bbox_extra_artists=(lgd,), bbox_inches='tight')

def make_plot(runs):
	"Plot results of timing trials"
	xp = numpy.linspace(10000, 100000, 100)
	for arg in runs:
		data = numpy.loadtxt(arg + ".txt")
		data = data.transpose()
		A = numpy.vstack([numpy.ones(len(data[0])), data[0] - numpy.ones(len(data[0])), numpy.ones(len(data[0]))/data[0]])
		a, b, c = numpy.linalg.lstsq(A.T, data[1])[0]
		print a, b, c
		plt.plot(data[0], data[1], '.', label="Measured", hold=True)
		plt.plot(data[0], numpy.dot(A.T, numpy.array([a, b, c])), '-', label=r"Model: $\alpha + \beta\cdot (p-1) + \frac{\gamma}{p}$"+"\n"+ r"$\alpha = " + str(a) + r"$,"+ "\n"+ r"$ \beta = " + str(b) + r"$," + "\n"+ r"$ \gamma = " + str(c) + r"$", hold=True)
	plt.xlabel('Number of Processors')
	plt.ylabel('Time (s)')

def show(runs):
	"Show plot of timing runs (for interactive use)"
	make_plot(runs)
	lgd = plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
	plt.show()

def main(runs):
	readData()
	m = fitModel()
	make_processor_plots(m)
	make_global_processor_plot(m)
	make_particles_plots(m)
	make_global_particle_plot(m)
	make_particles_plots_loglog(m)
	make_global_particle_plot_loglog(m)
	# "Show plot of timing runs (non-interactive)"
	# make_plot(runs)
	# lgd = plt.legend(bbox_to_anchor=(0.53, 0.95), loc=2, borderaxespad=0.)
	# plt.savefig(runs[0]+'.pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')

if __name__ == "__main__":
	main(sys.argv[1:])
