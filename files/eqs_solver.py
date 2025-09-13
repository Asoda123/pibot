from sympy import solve, Eq, symbols, simplify

x = symbols('x')
eq = ''
def solve_eq(us_eq):
    try:
        left_s, right_s = map(str.strip, us_eq.split('='))
        left_s = simplify(left_s)
        right_s = simplify(right_s)
        return solve(Eq(left_s,right_s),x)
    except Exception as e:
        return f'Error: {e}'
