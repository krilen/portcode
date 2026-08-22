import random

CODE_LENGTH = 4 # Default length of the code that should be generated
CODE_STAT = .4 # If the statistic of a number exceed it it will not be used.
OLDER_CODE_STAT = -20 # Number of previous older code that is used for the statistics


def create_random_code(length: int =CODE_LENGTH) -> str:
    """Function to generate a code (only numbers) of a certain length"""
    code = str(random.randint(0, int(str(9) *length)))

    code_length = len(code)

    if code_length < length:
        code = str((length - code_length) *"0") + code 

    return code


def check_random_code(code: int) -> bool:
    """Check that the numers within the code does not repeat more than once"""
    repeat = False
    verified = True

    code_str = str(code)

    # Make sure that the numbers ONLY repeats themself once
    # ex: 0012: OK, 0011: Not OK, 0001: Not OK, ...
    for i in range(len(code_str)):
        if i > 0:
            if code_str[i] == code[i -1] and not repeat :
                repeat = True
            elif code_str[i] == code[i -1] and repeat :
                verified = False  

    return verified


def load_used_codes(old_codes: str ="previous_codes.txt") -> list[str]:
    """Load the prevoius used codes so we dont reuse a code"""
    older_codes = []

    try:
        with open(old_codes, "r") as file:
            for line in file:

                try:
                    line_split = line.split(":")
                    old_code = int(line_split[1].strip())

                    # Save the older codes but make sure that they are saved ans stings
                    older_codes.append(str(old_code))

                # Making sure that the row is correct and the old code is a number
                except IndexError, ValueError:
                    continue

    except FileNotFoundError:
        print("!ERROR: File with previous older codes not found!")
    
    return older_codes


def create_older_codes_stat(codes: list[str]) -> map[int: float]:
    """Generate statistic of the numbers used in the previous code"""
    count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    stat = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0, 5: 0.0, 6: 0.0, 7: 0.0, 8: 0.0, 9: 0.0}

    for code in codes:
        for c in code:

            try:
                number = int(c)
                count[number] += +1

            except ValueError:
                continue

    count_sum = sum(count)

    if count_sum > 0:
        for i, number_count in enumerate(count):
            stat[i] = number_count / count_sum

    return stat


def main(length):
    "Main function to create and check the new suggested code"
    older_codes = load_used_codes() # The codes are a list of strings
    older_codes_stat = create_older_codes_stat(older_codes[OLDER_CODE_STAT:])

    #print(older_codes_stat)

    while True:
        code = create_random_code(length) # Returned as a string!

        # Is the randomness of the code good enough
        if not check_random_code(code):
            continue

        # Make sure that the code has not been used before
        if code in older_codes:
            continue

        # Make sure that randomness of the numbers within the same code is spread out
        check_code_stat = True

        for c in code:
            if older_codes_stat[int(c)] > CODE_STAT:
                check_code_stat = False
                break

        if not check_code_stat:
            print("Skip that one", code)
            continue

        break

    return code


if __name__ == "__main__":

    input_length = input("Provide the legth of the code (default is 4) >> ")

    if input_length == "":
        length = CODE_LENGTH

    else: 
        try: 
            length = int(input_length)

        except ValueError as e:
            print(f"Not a valid length, will use the default length!")
            length = CODE_LENGTH

    print("The random code that should be use is:", main(length))









    