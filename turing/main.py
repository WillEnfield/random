class state:
    def __init__(self, name, zero_instructions, one_instructions):
        self.name = name
        self.zero_instructions = zero_instructions
        self.one_instructions = one_instructions

    def get_instructions(self, symbol):
        if str(symbol) == "0":
            return self.zero_instructions
        elif str(symbol) == "1":
            return self.one_instructions
        else:
            raise ValueError("Symbol must be '0' or '1'")

class head:
    def __init__(self,position,starting_state):
        self.state = starting_state
        self.position = position
    
    def do_instructions(self, instructions, tape, states):

        tape[self.position] = int(instructions[0])

        if instructions[1] == "R":
            self.position += 1
        elif instructions[1] == "L":
            self.position -= 1
        elif instructions[1] == "N":
            pass
        else:
            raise ValueError("Direction must be 'R', 'L', or 'N'")
        
        if instructions[2] == "HALT":
            return "HALT"
        else:
            self.state = states[instructions[2]]

        return(tape)
        


tape = {}

state_a = state("a",
    zero_instructions=("1", "R", "b"),
    one_instructions=("1", "L", "HALT")
)

state_b = state("b",
    ("0","N","b"),
    ("1","R","a")
)

states = {
    "a": state_a,
    "b": state_b
}

turing_head = head(0, state_a)

i = 0

while True:

    cond_symbol = tape.get(turing_head.position,"0")

    instructions = turing_head.state.get_instructions(cond_symbol)
    tape = turing_head.do_instructions(instructions, tape, states)
    if tape == "HALT":
        break
    print(f"Iteration {i} done. Tape: {tape}")

    i += 1

print("Turing machine halted.")