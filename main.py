from src.parse_func import parse_func
from src.FEM_circle import animate_on_circle
from src.FEM_linear import animate_1D

import typer
from typing_extensions import Annotated

app = typer.Typer()

arb_func = Annotated[str, typer.Argument(help='arbitrary function of x and y that fits in a r=1 circle')]
arg_op = Annotated[float, typer.Argument(help='argument for defined function')]
ver_op = Annotated[bool, typer.Option('--new/--old', help='use old version with analytical method (default is FEM)')]

# simulation arguments
elements_op = Annotated[int, typer.Option(help='give approximate number of triangles to use in FEM')]
it_op = Annotated[int, typer.Option(help='# of iterations with dt time step')]
c_op = Annotated[float, typer.Option(help='speed of sound on membrane')]
dt_op = Annotated[float, typer.Option(help='time step in seconds between FEM frames')]
dir_op = Annotated[str, typer.Option(help='directory to store animations')]
show_op = Annotated[bool, typer.Option(help='show matplotlib window while rendering')]
save_op = Annotated[bool, typer.Option(help='save animation with ffmpeg to animations dir location')]


# def animate_2D(iterations: int, c: float, numTriangles: int, dt: float, dir: str, show: bool, save: bool, func) -> None:
@app.command()
def circle(func: arb_func = 'e - exp(x**2 + y**2)', 
           num_elements: elements_op = 50, iterations: it_op = 20000, 
           speed: c_op = 1, dt: dt_op = 0.001, dir: dir_op = 'animations', 
           show: show_op = False, save: save_op = True):
    if not show and not save:
        show = True
    try:
        user_func = parse_func(func)
    except:
        raise typer.Exit(1)
    print('all working good')
    animate_on_circle(iterations, speed, num_elements, dt, dir, show, save, user_func)

@app.command()
def line():
    print('will work on it')

if __name__ == "__main__":
    app()