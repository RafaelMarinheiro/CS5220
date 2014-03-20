We are using this model:

t(F, n, p) = F*(Beta*(p-1) + n(alpha + gamma/p))

Where 	F is the number of frames,
		n is the number of particles,
		p is the number of processors

In this model	alpha is the non-parallelizable portion of the code per particle
				beta is the communication overhead per each additional processor
				gamma is the parallelizable portion of the code per particle

The results of our experiments were obtained with F = 50, p = [1, ..., 8] and n = [1000, 2000, 4000, 8000, 16000]. When fitting that data with our model, we have obtained the following results:

alpha = 1.46423823204e-05
beta = 0.00397931763094
gamma = 0.000184113355164

Just run

	python plotter.py

to plot the graphs.