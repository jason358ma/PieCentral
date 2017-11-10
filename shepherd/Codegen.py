import random

def generate_challenge_code(seed):
    '''
    Given a random seed, generate a code corresponding to a random sequence of 
    concatenated functions for the students to decode and apply to RFID tags. 
    See student_decode() below.
    '''
    rand = random.Random(seed)
    
    code = 0
    
    # TODO: Actually write a proper generator. This is just a sample.
    for _ in range(5):
        code *= 10
        code += rand.randint(1, 2)
    
    return code
    
def student_func_mulfive(input):
    return input * 5
    
def student_func_addone(input):
    return input + 1

def student_decode(challenge_code, rfid_seed):
    '''
    Staff solution for the student decoder. Takes as input a code and the data 
    collected by an RFID scanner, and outputs the result of applying the 
    encoded functions onto that RFID "seed".
    '''
    func_map = {}
    func_map[1] = student_func_addone
    func_map[2] = student_func_mulfive
    
    code = challenge_code
    output = rfid_seed
    while code > 0:
        digit = code % 10
        code //= 10
        output = func_map[digit](output)
    
    return output
