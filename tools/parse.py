import argparse
import sys



def parse_command():

	def str2bool(value):
		if isinstance(value, bool):
			return value
		if value.lower() in ('yes', 'y', 'true', 't', '1'):
			return True
		elif value.lower() in ('no', 'n', 'false', 'f', '0'):
			return False
		else:
			raise argparse.ArgumentTypeError('Boolean value expected.')
		

	parser = argparse.ArgumentParser()

	parser.add_argument("-v", "--version", type=str, choices=['new', 'old'], default='new', help="old / new version of app, default = new")
	parser.add_argument("-c", "--config", type=str, default='config/params.txt', help="configuration file location")
	parser.add_argument("-d", "--dim", type=int, default=2, help="solve in 1 or 2 dimensions, default = 2")
	parser.add_argument("-it", "--iterations", type=int, default=20000, help="# of iterations with dt time step, default = 20000")
	parser.add_argument("--speed", type=int, default=5, help="speed of propagation through membrane (c), default = 1")
	parser.add_argument("--numElements", type=int, default=30, help="number of elements for FEM, default = 30")
	parser.add_argument("--dt", type=float, default=0.001, help="time step in seconds for iteration of FEM. default = 0.001")
	parser.add_argument("--dir", type=str, default='animations', help="directory to store animations")
	parser.add_argument("--show", type=str2bool, default=False, help="y/[N], show the animation in real time")
	parser.add_argument("--save", type=str2bool, default=True, help="[Y]/n save animation inside animation directory")


	args = parser.parse_args()

	return args.version, args.config, args.dim, args.iterations, args.speed, args.numElements, args.dt, args.dir, args.show, args.save