import numpy as np
import matplotlib.pyplot as plt

allowed_names = {
    'x' : None,
    'np' : np
}
y = None
USER_ID = None
file_name = None

def set_user_id(uid : int):
    global USER_ID
    global file_name
    USER_ID = str(uid)
    file_name = f'fig_{USER_ID}.png'

def eval_func(x_vals=None,func=None):
    allowed_names['x'] = x_vals
    try:
        return eval(func, {'__builtins__' : {}}, allowed_names)
    except Exception:
        return None

def get_f_n():
    return f'fig_{USER_ID}.png'

x = np.linspace(-10,10,200)
x = x[x != 0]
def set_y(func):
    global y
    y = eval_func(x,func=func)

    if y is not None:
        plt.figure(figsize=(6,10))
        plt.plot(x,y)
        plt.axvline(0, color='black')
        plt.axhline(0, color='black')
        plt.grid(True)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.savefig(f'fig_{USER_ID}.png')
        plt.close()
