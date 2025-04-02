import numexpr as ne
import numpy as np

"""
This is the best I could get from the internet. There were other options but they seemed unsafe.
will add more to safe_locals here when needed.
"""

class InvalidBoundary(Exception):
    """Custom exception to indicate an error in evaluating the function."""
    def __init__(self):
        super().__init__('invalid boundary condition')

safe_locals = {
    "e": np.e, "pi": np.pi
}

def is_zero_on_boundary(func) -> bool:
    for theta in np.linspace(0, 2*np.pi, 100):
        x = np.cos(theta)
        y = np.sin(theta)
        result = func(x, y)
        
        if not np.isclose(result, 0, atol=1e-6):  # Check if the result is close to zero
            print(f"Function did not evaluate to zero at theta = {theta:.3f} (x = {x:.3f}, y = {y:.3f}, result = {result})")
            return False # If any point on the unit circle is not zero, return False
        
    return True  # If all points on the circle are zero, return True


def parse_circle_func(raw_func: str):
    try:
        func = lambda x, y: ne.evaluate(raw_func, local_dict={**safe_locals, "x": x, "y": y})
        func(0,0) # test validity of function (check for syntax errors, etc.)
        # if not is_zero_on_boundary(func): # test if zero on boundary
        #     raise InvalidBoundary
        return func
    except Exception as e:
        print(f'exception raised: {e}')
        print('function is not valid, please try again.')
        raise e

def parse_line_func(raw_func: str):
    try:
        func = lambda x: ne.evaluate(raw_func, local_dict={**safe_locals, "x":x})
        func(0)

        return func
    except Exception as e:
        print(f'exception raised: {e}')
        print('function is not valid, please try again.')
        raise e
    

if __name__=='__main__':
    while True:
        raw_func = input('please enter a function of x and y:\n')
        func = parse_circle_func(raw_func)
        if func:
            print(func(1,1))
        
        raw_func = input('please enter a function of x:\n')
        func = parse_line_func(raw_func)
        if func:
            print(func(1))

