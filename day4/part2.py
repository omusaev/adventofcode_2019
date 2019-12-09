"""
An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the following are now true:

112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).
How many different passwords within the range given in your puzzle input meet all of the criteria?
"""

MIN = 372037
MAX = 905157


def _has_double(digits):
    prev = None
    occurrences = 0

    for digit in digits:
        if prev is None:
            prev = digit
            occurrences = 1
            continue

        if digit == prev:
            occurrences += 1
            continue
        else:
            if occurrences == 2:
                return True
            else:
                prev = digit
                occurrences = 1

    # the last two digits form a double (not triple)
    if occurrences == 2:
        return True

    return False


def _increasing_only(digits):
    return digits == sorted(digits)


def main():
    found = []
    for number in range(MIN, MAX + 1):
        digits = [int(digit) for digit in str(number)]

        if not _has_double(digits) or not _increasing_only(digits):
            continue

        found.append(number)

    print('The number of passwords: {}'.format(len(found)))


if __name__ == '__main__':
    main()
