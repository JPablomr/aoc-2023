DAY=3
INPUT_DIR='./inputs'

def read_input():
    # Create a generator by opening ./inputs/DAY.txt
    with open(f'{INPUT_DIR}/day{DAY}.txt') as f:
        for line in f:
            yield line.strip()

"""
--- Day 3: Gear Ratios ---

You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?

"""

import re

def part1():
    sum = 0
    input = read_input()
    previous = None
    current = next(input)
    forward = next(input)
    lookup = re.compile("(\.|[0-9])")

    while current:
        idx = 0
        start = 0
        while idx < len(current):
            if current[idx].isdigit():
                start = idx
                idx += 1
                # consume digits until we're at a non digit char
                while idx < len(current) and current[idx].isdigit():
                    idx += 1
                # now we know there's a number in current[start:idx]
                # Check current line, previous' and forward's [start-1:idx+1] for a symbol
                if start > 0:
                    min = start -1
                else:
                    min = 0 
                
                if idx+1 < len(current):
                    max = idx + 1
                else:
                    max = idx
                # Check current
                if re.sub(lookup, "", current[min:max]):
                     sum += int(current[start:idx])
                     idx +=1
                     continue
                # Check previous
                if previous and re.sub(lookup, "", previous[min:max]):
                     sum += int(current[start:idx])
                     idx +=1
                     continue
                # Check Forward
                if forward and re.sub(lookup, "", forward[min:max]):
                     sum += int(current[start:idx])
                     idx +=1
                     continue
            else:
                # Skip over any other chars
                idx += 1
        # Move the window forward
        previous = current
        current = forward
        forward = next(input, None)
    return sum

"""
--- Part Two ---

The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?

"""

from functools import reduce

def int_from_str(line, start_pos):
    """
    Move as far back as there are ints, also forward, then return the number
    """
    try:
        start = start_pos
        end = start_pos
        while start-1 >= 0 and line[start-1].isdigit():
            start -= 1
        while end+1 < len(line) and line[end+1].isdigit():
            end += 1
        if start == end:
            return int(line[start])
        else:
            return int(line[start:end+1])
    except:
        print(start_pos)
        print(start , end)
        print(line[start_pos])
        print(line)

def check_top_bottom(line, pos):
    numbers = []

    if line[pos].isdigit():
        numbers.append(int_from_str(line, pos))
    else:
        if pos > 0 and line[pos-1].isdigit():
            numbers.append(int_from_str(line, pos - 1))
        if pos+1 < len(line) and line[pos+1].isdigit():
            numbers.append(int_from_str(line, pos+1))
    return numbers  

def part2():
    sum = 0
    input = read_input()
    previous = None
    current = next(input)
    forward = next(input)

    while current:
        idx = 0
        while idx < len(current):
            if current[idx] != '*':
                idx += 1
                continue
            adjacent_gears = check_top_bottom(current, idx)
            # Check the bounding box for matches, if we have more than 2, discard
            # top and bottom checks:
            if previous:
                adjacent_gears += check_top_bottom(previous, idx)
            if forward:
                adjacent_gears += check_top_bottom(forward, idx)
            
            if len(adjacent_gears) == 2:
                sum += reduce(lambda x,y:x*y, adjacent_gears)
            idx += 1
        # Move the window forward
        previous = current
        current = forward
        forward = next(input, None)
    return sum

print("Part 1")
print(f"Sum is {part1()}")

print("Part 2")
print(f"Sum is {part2()}")