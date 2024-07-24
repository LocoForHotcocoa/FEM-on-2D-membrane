import src.wave_main as new
import oldsrc.old_main as old
from tools.parse import *

# parsing command line args
version, config, dim, iterations, c, numElements, dt, dir, show, save = parse_command()

if version == 'old':
	old.animate_2D(config)

if version == 'new':
	if dim == 1:
		new.animate_1D(iterations, c, numElements, dt, dir, show, save)
	if dim == 2:
		new.animate_2D(iterations, c, numElements, dt, dir, show, save)


