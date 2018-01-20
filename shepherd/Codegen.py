import random

class Codegen:

    def __init__(self, rfids, rand_seed=None):
        '''
        Manages the generated code and rfid-answer pairs.
        `rfids` must be an iterable of RFID ints.
        Duplicate RFIDs in the provided iterable are ignored.
        '''

        # Seed our local RNG
        self._random = random.Random(rand_seed)
        rfids = set(rfids) # Ignore duplicates

        # Keep generating random codes until we get one that gives a one-to-one
        # mapping between RFIDs and answers
        while True:
            self._rfid_to_ans = {}
            self._ans_to_rfid = {}
            self._code = generate_challenge_code(self._random)
            # We want there to be a one-to-one mapping between RFIDs and answers
            # Therefore only break the loop if we randomly generate a code
            # that produces unique answers for every RFID in the list
            duplicate_answers = False
            for rfid in rfids:
                solution = staff_decode(self._code, rfid)
                if solution in self._ans_to_rfid:
                    duplicate_answers = True
                    break
                self._ans_to_rfid[solution] = rfid
                self._rfid_to_ans[rfid] = solution
            if not duplicate_answers:
                break
        # This is always true since we guaranteed above that
        # the (rfid --> solution) mapping is bijective
        assert len(self._rfid_to_ans) == len(self._ans_to_rfid)

    def check_solution(self, solution):
        '''
        Returns which RFID that the solution corresponds to
        return None if it doesn't match any.
        '''
        return self._ans_to_rfid.get(solution, None)

    def get_code(self):
        '''
        Get the challenge code to be sent to students
        '''
        return self._code

    def get_solution(self, rfid):
        '''
        Returns which solution that the RFID corresponds to
        return None if it doesn't match any.

        >>> c = Codegen([1, 2, 3], 0)
        >>> c.check_solution(c.get_solution(1))
        1
        >>> c.check_solution(c.get_solution(2))
        2
        >>> c.check_solution(c.get_solution(3))
        3
        '''
        return self._rfid_to_ans.get(rfid, None)

# Various ideas for functions for the students
# Included are example student implementations
# Of course, the example solutions are optimized
# for pedagogical simplicity, not runtime speed or memory

# Functions presented in no particular order of difficulty
# Both inputs and outputs guaranteed to be nonnegative integers

def next_power(num):
    '''
    The next biggest (whole) power of two

    >>> next_power(2)
    2
    >>> next_power(3)
    4
    >>> next_power(23)
    32
    >>> next_power(2557)
    4096
    >>> next_power(12510)
    16384
    >>> next_power(0)
    1
    '''
    solution = 1
    while solution < num:
        solution = solution * 2
    return solution
def reverse_digits(num):
    '''
    The number with digits reversed

    >>> reverse_digits(2)
    2
    >>> reverse_digits(3)
    3
    >>> reverse_digits(23)
    32
    >>> reverse_digits(2557)
    7552
    >>> reverse_digits(12510)
    1521
    >>> reverse_digits(0)
    0
    '''
    solution = 0
    while num > 0:
        solution = solution * 10
        solution = solution + (num % 10)
        num = num // 10
    return solution
def smallest_prime_fact(num):
    '''
    Smallest prime factor

    >>> smallest_prime_fact(2)
    2
    >>> smallest_prime_fact(3)
    3
    >>> smallest_prime_fact(3127)
    53
    >>> smallest_prime_fact(2557)
    2557
    >>> smallest_prime_fact(1251)
    3
    >>> smallest_prime_fact(0)
    0
    >>> smallest_prime_fact(1)
    1
    '''
    for i in range(2, num):
        if num % i == 0:
            return i
    return num
def prime_factor(num):
    '''
    Output a concatenated sequence of prime factors

    >>> prime_factor(2)
    2
    >>> prime_factor(3)
    3
    >>> prime_factor(2 * 3)
    23
    >>> prime_factor(2 * 5 * 5 * 7)
    2557
    >>> prime_factor(12510)
    2335139
    >>> prime_factor(1)
    0
    '''
    solution = '0'
    while num > 1:
        for divisor in range(2, num + 1):
            if num % divisor == 0:
                solution = solution + str(divisor)
                num = num // divisor
                break
    return int(solution)
def silly_base_two(num):
    '''
    Convert to base two (with digits interpreted as if in base ten)

    >>> silly_base_two(2)
    10
    >>> silly_base_two(3)
    11
    >>> silly_base_two(3127)
    110000110111
    >>> silly_base_two(2557)
    100111111101
    >>> silly_base_two(1251)
    10011100011
    >>> silly_base_two(0)
    0
    '''
    output = 0
    place = 0
    while num > 0:
        bit = num % 2
        num = num // 2
        output += bit * (10 ** place)
        place += 1
    return output
def most_common_digit(num):
    '''
    Every digit in the input occurs N times. (exclude zero)
    Output the digit with the greatest N.
    (If there is a tie, use the largest digit)
    Return that (digit + 10) raised to the power of (N x 2)

    Special case: zero should just output 100.

    >>> most_common_digit(2)
    144
    >>> most_common_digit(3)
    169
    >>> most_common_digit(3127)
    289
    >>> most_common_digit(2557)
    50625
    >>> most_common_digit(1251)
    14641
    >>> most_common_digit(111222333444)
    7529536
    >>> most_common_digit(314159265358979324)
    47045881
    >>> most_common_digit(0)
    100
    '''
    counts = {}
    for digit in range(0, 10):
        counts[digit] = 0
    while num > 0:
        digit = num % 10
        num = num // 10
        counts[digit] += 1
    output = 0
    biggest_count = 1
    for digit in range(1, 10):
        if counts[digit] >= biggest_count:
            biggest_count = counts[digit]
            output = digit
    return (output + 10) ** (biggest_count * 2)
def valid_isbn_ten(num):
    '''
    ISBN-10 validation: Check that the given ISBN-10 number is valid.
    Return the number if it is valid, or the next integer after which is valid.
    Use only the bottom 10 digits if the input is longer than 10 digits.
    Use zeros in place of missing digits if the input is shorter than 10 digits.

    >>> valid_isbn_ten(2)
    19
    >>> valid_isbn_ten(3)
    19
    >>> valid_isbn_ten(128122765)
    128122765
    >>> valid_isbn_ten(128122760)
    128122765
    >>> valid_isbn_ten(60)
    78
    >>> valid_isbn_ten(123456788)
    123456789
    '''
    valid = False
    while not valid:
        total = 0
        digit_list = num
        for i in range(0, 10):
            digit = digit_list % 10
            digit_list = digit_list // 10
            total += digit * (10 - i)
        valid = total % 11 == 0
        if not valid:
            num += 1
    return num
def simd_four_square(num):
    '''
    Evenly divide the input digits into four groups, treating each group as if
    it were its own integer. Square each group, and then rejoin the squared
    integers into a single value such that the total number of digits within
    each group is preserved. If the number of input digits is not evenly
    divisible by four, pad the left of the input with as few zeros necessary
    until the input digit count is evenly divisble by four.

    >>> simd_four_square(3210)
    9410
    >>> simd_four_square(11121314)
    21446996
    >>> simd_four_square(54321) # treat as "00054321"
    254941
    >>> simd_four_square(0)
    0
    '''
    num_digits = 1
    while num // (10 ** num_digits) > 0:
        num_digits += 1

    if num_digits % 4 != 0:
        num_digits += 4 - (num_digits % 4)

    group_len = num_digits // 4

    output = 0

    for group_idx in [3, 2, 1, 0]:
        group = (num // (10 ** (group_idx * group_len))) % (10 ** group_len)
        squared = (group * group) % (10 ** group_len)
        output *= 10 ** group_len
        output += squared

    return output
def double_caesar_cipher(key):
    '''
    Use the given input as a double-caesar-cipher encryption key for the first
    ten digits of pi. If the key is not long enough, reuse it to encrypt the
    unencrypted digits, starting from the least significant digit.

    >>> double_caesar_cipher(0)
    3141592653
    >>> double_caesar_cipher(1)
    4252603764
    >>> double_caesar_cipher(9677799275)
    2718281828
    >>> double_caesar_cipher(10000000000)
    3141592653
    >>> double_caesar_cipher(3141592653)
    6282084206
    >>> double_caesar_cipher(12136)
    4354104789
    >>> double_caesar_cipher(969518457)
    0
    >>> double_caesar_cipher(123)
    6264615776
    '''
    msg = 3141592653
    pi_str = str(msg)
    key_str = str(key)
    # expand key_str to be at least as long as pi_str
    key_str *= (len(pi_str) // len(key_str)) + 1
    result = ''
    for i in range(len(pi_str)):
        ciph = (int(pi_str[-1 - i]) + int(key_str[-1 - i])) % 10
        result = str(ciph) + result
    return int(result)

def generate_challenge_code(rand):
    '''
    Generates a code corresponding to a random sequence of
    concatenated functions for the students to decode and apply to RFID tags.
    See student_decode() below.
    '''
    # Need to actually write a proper generator. This is just a sample.
    code = 0
    for _ in range(5):
        code *= 10
        code += rand.randint(1, 8)
    return code

def staff_decode(challenge_code, rfid_seed):
    '''
    Staff solution for the student decoder. Takes as input a code and the data
    collected by an RFID scanner, and outputs the result of applying the
    encoded functions onto that RFID "seed".
    '''

    # No preprocessing
    identity = lambda x: x

    # Generate a function to limit size of inputs
    def limit_input_to(limit):
        def retval(input_val):
            while input_val > limit:
                input_val = (input_val % limit) + (input_val // limit)
            return input_val
        return retval

    # Pairs of student-made functions and pre-processors run on input beforehand
    func_map = {}
    func_map[1] = (next_power, identity)
    func_map[2] = (reverse_digits, identity)
    func_map[3] = (smallest_prime_fact, limit_input_to(1000000))
    func_map[4] = (double_caesar_cipher, identity)
    func_map[5] = (silly_base_two, identity)
    func_map[6] = (most_common_digit, identity)
    func_map[7] = (valid_isbn_ten, identity)
    func_map[8] = (simd_four_square, identity)

    code = challenge_code
    output = ''
    while code > 0:
        digit = code % 10
        code //= 10

        func = func_map[digit][0]
        preprocess = func_map[digit][1]

        output += '555' + str(func(preprocess(rfid_seed)))

    return int(output)

def _debug_random_sample(sample_size):
    # Random sampling of codes, finds how frequent each digit is
    count = {}
    total = 0
    for i in range(1, 9):
        count[i] = 0
    rng = random.Random(0)
    rfids = [rng.randint(0, 999999999999999) for _ in range(0, 5)]
    for i in range(0, sample_size):
        code = Codegen(rfids, i).get_code()
        while code > 0:
            digit = code % 10
            code //= 10
            count[digit] += 1
            total += 1
    for i in range(1, 9):
        count[i] /= total
    return count
