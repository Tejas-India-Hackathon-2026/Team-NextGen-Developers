from modules.calculator_engine import evaluate_math_expression

def test_math_eval():
    res, err = evaluate_math_expression('10 + 20 * 3')
    assert err is None
    assert res == 70

def test_prohibited_token():
    res, err = evaluate_math_expression('__import__("os")')
    assert res is None
    assert 'Prohibited' in err
