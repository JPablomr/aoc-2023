# Library-ish things
DAY=1
INPUT_DIR='./inputs'

def read_input():
    # Create a generator by opening ./inputs/DAY.txt
    with open(f'{INPUT_DIR}/day{DAY}.txt') as f:
        for line in f:
            yield line.strip()

"""
--- Day 1: Trebuchet?! ---

Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?

"""


def calibration_value(line):
    start_digit = None
    end_digit = None
    for char in line:
        if char.isdigit():
            if start_digit is None:
                start_digit = char
            end_digit = char
    return int(f"{start_digit}{end_digit}")

def part1():
    sum = 0
    for line in read_input():
        sum += calibration_value(line)
    return sum


"""
--- Part Two ---

Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.
"""

def calibrate_with_text(line):
    idx = 0

    start_digit = None
    end_digit = None

    def add_number(number):
        nonlocal start_digit, end_digit
        if not start_digit:
            start_digit = number
        end_digit = number

    def matches(number):
        if idx+len(number) > len(line):
            return False
        try:
            return line[idx:idx+len(number)] == number
        except:
            return False

    while idx < len(line):
        c = line[idx]
        if c.isdigit():
            add_number(c)
            idx += 1
            continue

        match c:
            case 'o':
                if matches("one"):
                    add_number("1")
                    idx += 2 # The end char can be the start of another number, so dumb
                else:
                    idx += 1
            case 't':
                if matches("two"):
                    add_number("2")
                    idx += 2
                elif matches("three"):
                    add_number("3")
                    idx += 4
                else:
                    idx += 1
            case 'f':
                if matches("four"):
                    add_number("4")
                    idx += 3
                elif matches("five"):
                    add_number("5")
                    idx += 3
                else:
                    idx += 1
            case 's':
                if matches("six"):
                    add_number("6")
                    idx += 2
                elif matches("seven"):
                    add_number("7")
                    idx += 4
                else:
                    idx += 1
            case 'e':
                if matches("eight"):
                    add_number("8")
                    idx += 4
                else:
                    idx += 1
            case 'n':
                if matches("nine"):
                    add_number("9")
                    idx += 3
                else:
                    idx += 1
            case _:
                idx+=1
    return int(f"{start_digit}{end_digit}")
 
 def part2():
    sum = 0
    for line in read_input():
        sum += calibrate_with_text(line)
    return sum


print("Part 1")
print(f"Sum is {part1()}")

print("Part 2")
print(f"Sum is {part2()}")