#! /usr/bin/env python3
import io
import sys
import struct
import array

# Architecture definition
memory    = array.array('H', [0] * 0xFFFF)
registers = array.array('H', [0] * 16)
SP = 14
PC = 15
registers[SP] = 0xFFFF

# Instructions definition
def instr_add(i, j, k):
    registers[i] = registers[j] + registers[k]

def instr_mul(i, j, k):
    registers[i] = registers[j] * registers[k]

def instr_sub(i, j, k):
    registers[i] = registers[j] - registers[k]

def instr_div(i, j, k):
    registers[i] = int(registers[j] / registers[k])

def instr_cop(i, j, ign):
    registers[i] = registers[j]

def instr_afc(i, j, ign):
    registers[i] = j

def instr_load(i, j, ign):
    registers[i] = memory[j]

def instr_str(i, j, ign):
    memory[i]    = registers[j]

def instr_equ(i, j, k):
    registers[i] = 1 if registers[j] == registers[k] else 0

def instr_inf(i, j, k):
    registers[i] = 1 if registers[j] <  registers[k] else 0

def instr_infe(i, j, k):
    registers[i] = 1 if registers[j] <= registers[k] else 0

def instr_sup(i, j, k):
    registers[i] = 1 if registers[j] >  registers[k] else 0

def instr_supe(i, j, k):
    registers[i] = 1 if registers[j] >= registers[k] else 0

def instr_jmp(i, ign1, ign2):
    registers[PC] = i-4

def instr_jmpc(i, j, ignZ):
    if registers[j] == 0:
        registers[PC] = i-4

def instr_pop(i, ign1, ign2):
    registers[i] = memory[registers[SP]]
    registers[SP] = registers[SP] + 1

def instr_push(i, ign1, ign2):
    registers[SP] = registers[SP] - 1
    memory[registers[SP]] = registers[i]

# Indirection table from opcodes to instruction implementations
opc2instr = {
    0x01: instr_add,
    0x02: instr_mul,
    0x03: instr_sub,
    0x04: instr_div,
    0x05: instr_cop,
    0x06: instr_afc,
    0x07: instr_load,
    0x08: instr_str,
    0x09: instr_equ,
    0x0A: instr_inf,
    0x0B: instr_infe,
    0x0C: instr_sup,
    0x0D: instr_supe,
    0x0E: instr_jmp,
    0x0F: instr_jmpc,
    0x10: instr_pop,
    0x11: instr_push
}

# Registers-level debugging, used after every instruction
def print_registers():
    i = 0
    first_line  = "| "
    second_line = "| "
    while i < 16:
        reg_name = "R" + str(i) if i < SP else "SP" if i == SP else "PC"
        reg_val  = str(registers[i])

        first_line = first_line + reg_name.ljust(5) + " | "
        second_line = second_line + reg_val.ljust(5) + " | "

        i = i+1

    print(first_line)
    print(second_line)

# Gives usage instructions if not used correctly
if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " code")
    exit(1)

# Loads the given program into memory
input_path = sys.argv[1]
fio = io.FileIO(input_path)
fio.readinto(memory)

# Interprets each instruction sequentially
while True:
    pc = registers[PC]

    opcode = memory[pc]
    op1    = memory[pc+1]
    op2    = memory[pc+2]
    op3    = memory[pc+3]
    instr_hdlr = opc2instr.get(opcode)
    if instr_hdlr:
        instr_hdlr(op1, op2, op3)
    else:
        exit(0)

    print_registers()
    input("Press enter to continue...")
    registers[PC] = registers[PC] + 4
