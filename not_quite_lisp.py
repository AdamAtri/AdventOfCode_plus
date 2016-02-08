import argparse
import re

###########################
# Day 1
###########################
def santa():
    parser = argparse.ArgumentParser(description='What are santa\'s instructions:')
    parser.add_argument('-ins',  help='a string containing santa\'s instructions')

    args = parser.parse_args()
    instructions = args.ins
    floor = 0
    first_trip_to_basement = None

    for i, l in enumerate(instructions):
        if l == "(":
            floor += 1
        elif l == ")":
            floor -= 1
            if floor == -1:
                print 'basement', i+1
                if first_trip_to_basement is None:
                    first_trip_to_basement = i+1

    print 'Floor:', floor, '\nFirst Trip to Basement:', first_trip_to_basement

###########################
# Day 2
###########################
def order_wrappings():
    parser = argparse.ArgumentParser(description='What are santa\'s instructions:')
    parser.add_argument('--order', help='the order filename')
    parser.add_argument('-paper', help='process order for paper(True|False)')
    parser.add_argument('-ribbon', help='process order for ribbon(True|False)')
    args = parser.parse_args()

    order_file = args.order
    paper_footage = None
    ribbon_footage = None
    if args.paper:

        paper_footage = get_paper_total(order_file)
    if args.ribbon:
        ribbon_footage = get_ribbon_total(order_file)

    message = '*'*10 + 'TOTAL' + '*'*10
    message += '\n*\tPaper: ' + (str(paper_footage) if paper_footage is not None else '0.0')
    message += '\n*\tRibbon: ' + (str(ribbon_footage) if ribbon_footage is not None else '0.0')
    print message


def _get_dimension_array(order_file):
    with open(order_file, 'r') as orders:
        total_dimensions = orders.read()

    total_sq_foots = 0
    dimension_array = total_dimensions.split("\n")

    pattern = '(\d+)x(\d+)x(\d+)'
    result = []
    for x in dimension_array:
        matches = re.search(pattern, x)
        if matches:
            l = int(matches.group(1))
            w = int(matches.group(2))
            h = int(matches.group(3))
            result.append([l, w, h])
        else:
            print 'BAD:', x
    return result

def get_paper_total(order_file):
    dimension_array = _get_dimension_array(order_file)
    total_sq_foots = 0
    for d in dimension_array:
        print d
        l, w, h = d
        total_sq_foots += calculate_sq_f(l, w, h)
    return total_sq_foots

def get_ribbon_total(order_file):
    dimension_array = _get_dimension_array(order_file)
    total_ribbon_length = 0
    for r in dimension_array:
        total_ribbon_length += calculate_r_length(r)
    return total_ribbon_length

def calculate_sq_f(l, w, h):
    top_bottom = 2 * l * w
    front_back = 2 * w * h
    sides = 2 * l * h
    extra = int(min(top_bottom,front_back, sides)/2)
    return (top_bottom + front_back + sides + extra)

def calculate_r_length(dimensions):
    dimensions.sort()
    wrap = dimensions[0]*2 + dimensions[1]*2
    bow = dimensions[0] * dimensions[1] * dimensions[2]
    return wrap + bow

##########################
# Day 3 Perfectly Spherical Houses in a Vacuum
#########################
def delivery_route():
    parser = argparse.ArgumentParser(description='What are santa\'s instructions:')
    parser.add_argument('--directions', help='give santa a direction sheet')
    args = parser.parse_args()
    dir_file = args.directions

    with open(dir_file, 'r') as df:
        directions = df.read()

    santa = [0, 0]
    robo = [0, 0]

    houses = {tuple(santa):1}

    for i, d in enumerate(directions):
        who, ho = (santa, 'santa') if i % 2 == 0 else (robo, 'robo')
        if d == '<':
            who[0] -= 1
        elif d == '>':
            who[0] += 1
        elif d == '^':
            who[1] += 1
        elif d == 'v':
            who[1] -= 1
        loc = tuple(who)
        if loc in houses:
            houses[loc] += 1
        else:
            houses[loc] = 1

    print 'Number of directions:' + str(len(directions))
    print 'Number of houses:' + str(len(houses))

############################
# Day 4: The Ideal Stocking Stuffer
############################
def hash_miner():
    from hashlib import md5
    parser = argparse.ArgumentParser(description='What are santa\'s instructions:')
    parser.add_argument('--key', help='The AdventCoin hash key')
    args = parser.parse_args()
    key = args.key

    i = 1
    result = None
    while True:
        hash = md5(key + str(i))
        if hash.hexdigest().startswith('000000'):
            break
        i += 1

    print 'Hash result:', i

###########################
# Day 5: Doesn't He Have Intern-Elves for This?
###########################

def naughty_list():
    parser = argparse.ArgumentParser(description='Getting the NICE strings')
    parser.add_argument('-l', '--listname', help='santa needs his list')
    args = parser.parse_args()
    list_file = args.listname

    with open(list_file, 'r') as naught_or_nice:
        the_names_raw = naught_or_nice.read()

    the_names = the_names_raw.split("\n")
    nice = []
    for name in the_names:
        if not _has_repeating_groups(name):
            print 'no repeating groups:', name
            continue
        if not _has_repeating_letter(name):
            print 'no repeating letters:', name
            continue
        nice.append(name)

    print "NICE:", str(len(nice))

def _search_string(pattern, string):
    rgx = re.compile(pattern)
    matches = rgx.search(string)
    return matches

def _has_repeating_groups(name):
    pattern = r"(?:(.{2,}).*\1)"
    matches = _search_string(pattern, name)
    return matches is not None

def _has_repeating_letter(name):
    pattern = r"(?:(.).)\1"
    matches = _search_string(pattern, name)
    return matches is not None

def _has_three_vowels(name):
    pattern = "(a|e|i|o|u)"
    matches = re.findall(pattern, name)
    return len(matches) >= 3

def _has_double(name):
    pattern = r"(.)\1{1,}"
    matches = re.findall(pattern, name)
    return len(matches) >= 1

def _has_no_excluded(name):
    pattern = "^((?!ab|cd|pq|xy).)*$"
    matches = _search_string(pattern, name)
    return matches is not None

###############################
# Day 6: Probably a Fire Hazard
###############################
TURN_ON = 'turn on '
TURN_OFF = 'turn off '
TOGGLE = 'toggle '
def working_with_light_matrix():
    parser = argparse.ArgumentParser(description='Getting the NICE strings')
    parser.add_argument('-i', '--instructions', help='tis the season of festive lights')
    parser.add_argument('-b', '--bright', help='get the brightness')
    args = parser.parse_args()
    inst_file = args.instructions
    bright = args.bright if args.bright else False

    with open(inst_file, 'r') as in_file:
        instructions_raw = in_file.read()
    instructions = instructions_raw.split("\n")

    grid = _make_grid()

    for instruction in instructions:
        dir_rect = _parse_instruction(instruction)
        if dir_rect is None:
            continue
        direction, top_left, btm_right = dir_rect
        _update_grid(grid, direction, top_left, btm_right, for_brightness=bright)

    if bright:
        print "That was bright, in fact it was this bright: " + str(_get_light_brightness(grid))
    else:
        print "Total lit after that light show: " + str(_get_light_count(grid))

def _make_grid():
    """
    Returns a 2d array 1000x1000 in size
    :return:
    """
    grid = [[0 for y in range(1000)] for x in range(1000)]
    return grid


def _parse_instruction(instruction):
    finish = 0
    for i, s in enumerate(instruction):
        if s.isdigit():
            finish = i
            break
    direction = instruction[:finish]
    raw_rect_corners = instruction[finish:]
    corners = raw_rect_corners.split(' through ')
    if ',' not in corners[0]:
        return None
    x, y = corners[0].split(',')
    top_left = (int(x), int(y))
    x, y = corners[1].split(',')
    btm_right = (int(x), int(y))
    result = (direction, top_left, btm_right)
    return result

def _update_grid(grid, direction, top_left, btm_right, for_brightness=False):
    x_min, y_min = top_left
    x_max, y_max = btm_right
    # visualize working from left to right, top to bottom
    y = y_min
    while y <= y_max:
        x = x_min
        while x <= x_max:
            if for_brightness:
                value = 1 if direction == TURN_ON else -1 if direction == TURN_OFF else 2
                # the minimum brightness value for any light is 0
                grid[x][y] = max(grid[x][y] + value, 0)
            else:
                value = 1 if direction == TURN_ON else 0 if direction == TURN_OFF else None
                if value is None:
                    value = 0 if grid[x][y] == 1 else 1
                grid[x][y] = value
            x += 1
        y += 1

def _get_light_count(grid, state=1):
    count = 0
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            if grid[x][y] == state:
                count += 1
    return count

def _get_light_brightness(grid):
    brightness = 0
    for x in range(len(grid)):
        for y in range(len(grid[x])):
            brightness += grid[x][y]
    return brightness


#################################
# Day 7: Some Assembly Required (bitwise operations)
#################################
bit_dict = dict(AND=lambda x, y: x & y,
                OR=lambda x, y: x | y,
                LSHIFT=lambda x, shift: x << shift,
                RSHIFT=lambda x, shift: x >> shift,
                NOT=lambda x: ~x)
def main():
    parser = argparse.ArgumentParser(description='Getting the NICE strings')
    parser.add_argument('-i', '--gates', help='circuits and wires')
    parser.add_argument('-r', '--repeat', help='repeat this sequence')
    args = parser.parse_args()

    repeat = args.repeat

    gates_file = args.gates
    with open(gates_file, 'r') as gf:
        gates_raw = gf.read()
    gates_instructions = gates_raw.split('\n')

    gates = dict()
    incomplete_instructions = []
    _prepare_instructions(incomplete_instructions, gates_instructions)
    count = 0
    while len(incomplete_instructions) > 0:
        instruction = incomplete_instructions.pop(0)
        if instruction is None:
            continue
        if not _evaluate_instruction(instruction, gates):
            incomplete_instructions.append(instruction)
        print '%s. Incomplete instructions:' % str(count), str(len(incomplete_instructions))
        if len(incomplete_instructions) == 0 and repeat:
            print '_____Now for round 2_____'
            repeat = False
            b_value = gates['a']
            gates = dict(b=b_value)
            _prepare_instructions(incomplete_instructions, gates_instructions)
        count += 1

    print ('The value of "a":', gates['a'])

def _prepare_instructions(new_list, raw_instructions):
    # parse each of the raw instructions and append it's parsed value to the
    # incomplete_instructions list
    for gate in raw_instructions:
        result = _parse_gate(gate)
        if result:
            new_list.append(result)


def _parse_gate(in_gate):
    # verify that the in_gate instruction contains the assignment notation
    if '->' not in in_gate:
        return None
    # split the gate instruction on the assignment notation
    parts = in_gate.split('->')
    # part 0 contains the raw expression that will produce a value for the key
    expression = parts[0].strip()
    key = parts[1].strip()
    result = (key, expression)
    return result

def _evaluate_instruction(instruction, gates):
    # if the gate_key is already in the gates dict,
    # DO NOT REASSIGN
    gate_key = instruction[0]
    if gate_key in gates:
        return True
    # get the raw expression (instructions[1]) split into parts
    exp_parts = instruction[1].split(" ")
    i = 0
    f = None
    # find the function
    for i, part in enumerate(exp_parts):
        if part in bit_dict:
            f = bit_dict[part]
            break
    value = None
    # if there is no function then just assign the
    # value in the expression
    if f is None:
        value = _eval_operand(exp_parts[0], gates)
    # else, if the function is NOT then check that the
    # remaining expression part is a valid key or digit
    elif i == 0:
        op = _eval_operand(exp_parts[1], gates)
        if op is not None:
            value = f(op)
    # if i == 1 then f is AND, OR, LSHIFT, or RSHIFT
    elif i == 1:
        if len(exp_parts) < 3:
            print ('WTF?????', exp_parts)
        op1 = _eval_operand(exp_parts[0], gates)
        op2 = _eval_operand(exp_parts[2], gates)
        if op1 is not None and op2 is not None:
            value = f(op1, op2)
    else:
        print ('OOPS>>>', exp_parts)
    if value is None:
        return False
    gates[gate_key] = value
    return True


def _eval_operand(part, gates):
    if part.isdigit():
        return int(part)
    elif part in gates:
        return gates[part.strip()]
    else:
        return None


if __name__ == '__main__':
    main()
