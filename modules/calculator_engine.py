import math

def evaluate_math_expression(expr_str: str) -> tuple:
    if not expr_str:
        return None, 'Empty expression'
    disallowed = ['__', 'import', 'exec', 'eval', 'open', 'os', 'sys']
    for d in disallowed:
        if d in expr_str.lower():
            return None, f'Prohibited operation: {d}'
    try:
        safe = {'abs': abs, 'round': round, 'min': min, 'max': max, 'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos}
        clean = expr_str.replace('×', '*').replace('÷', '/').replace('^', '**')
        return eval(clean, {'__builtins__': {}}, safe), None
    except Exception as e:
        return None, str(e)
