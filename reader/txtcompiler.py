class error:
    def __init__(self, message):
        self.message = message

def isnumber(value):
    try:
        float(value)
    except ValueError:
        return False
    else:
        return True


def evaluate(expression, variables):
    if expression.startswith("<") and expression.endswith(">"):
        calculated = calculate(expression[1:-1], variables)
        if type(calculated) == error:
                return calculated
        else:
            return calculated
    elif expression.startswith('"') and expression.endswith('"'):
        return expression[1:-1]
    elif expression in variables:
        return variables[expression]
    else:
        return error("Unnknown expression")



def calculate(expression, variables):
    #tokenize
    tokens = expression.replace("(", " ( ").replace(")", " ) ").replace("+", " + ").replace("-", " - ").replace("*", " * ").replace("/", " / ").replace("^", " ^ ").split()
    for i in range(len(tokens)):
        if isnumber(tokens[i]):
            tokens[i] = float(tokens[i])
        elif tokens[i] in variables:
            tokens[i] = variables[tokens[i]]
        elif tokens[i] in ["+", "-", "*", "/", "^", "(", ")"]:
            pass
        else:
            return error("Unknown token: " + tokens[i])
    #convert to postfix
    output_RPN = []
    holding_stack = []
    while len(tokens) != 0:
        token = tokens.pop(0)
        if isnumber(token):
            output_RPN.append(token)
        elif token in ["+", "-", "*", "/", "^"]:
            while (len(holding_stack) > 0 and holding_stack[-1] in {"+":1, "-":1, "*":2, "/":2, "^":3, "(":0} and (({"+":"L", "-":"L", "*":"L", "/":"L", "^":"R"}[token] == "L" and {"+":1, "-":1, "*":2, "/":2, "^":3, "(":0}[holding_stack[-1]] >= {"+":1, "-":1, "*":2, "/":2, "^":3, "(":0}[token]) or ({"+":"L", "-":"L", "*":"L", "/":"L", "^":"R"}[token] == "R" and {"+":1, "-":1, "*":2, "/":2, "^":3, "(":0}[holding_stack[-1]] > {"+":1, "-":1, "*":2, "/":2, "^":3, "(":0}[token]))):
                output_RPN.append(holding_stack.pop())
            holding_stack.append(token)
        elif token == "(":
            holding_stack.append(token)
        elif token == ")":
            while len(holding_stack) > 0 and holding_stack[-1] != "(":
                output_RPN.append(holding_stack.pop())
            if len(holding_stack) == 0:
                return error("Mismatched parentheses")
            holding_stack.pop()

    while holding_stack:
        if holding_stack[-1] in ("(", ")"):
            return error("Mismatched parentheses")
        output_RPN.append(holding_stack.pop())
    #evaluate postfix
    output = []
    for token in output_RPN:
        if type(token) == int or type(token) == float:
            output.append(token)
        elif token in ["+", "-", "*", "/", "^"]:
            if len(output) < 2:
                return error("Invalid expression")
            b = output.pop()
            a = output.pop()
            if token == "+":
                output.append(a + b)
            elif token == "-":
                output.append(a - b)
            elif token == "*":
                output.append(a * b)
            elif token == "/":
                output.append(a / b)
            elif token == "^":
                output.append(a ** b)
    if len(output) > 1:
        return error("Unknown error")
    return output[0]

def txt_compiler(content):
    print("Compiling and running the .txt file...")
    content = content.replace("\n", "").replace("\r", "").replace("\t", "").replace("    ", "").replace(" ","")
    lines = content.split(";")
    variables = {}
    for line in lines:
        #variable declaration
        if line.startswith("var"):
            parts = line[3:].split("=")
            if len(parts) == 2:
                evaluated = evaluate(parts[1], variables)
                if type(evaluated) != error:
                    variables[parts[0]] = evaluated
                else:
                    print("Line: '" + line + "' failed with error '" + evaluated + "'")

txt_compiler("var a = <1+2>; var b = a; wasdw")