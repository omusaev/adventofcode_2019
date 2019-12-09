"""
It is a six-digit number.
The value is within the range given in your puzzle input.
Two adjacent digits are the same (like 22 in 122345).
Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
Other than the range rule, the following are true:

111111 meets these criteria (double 11, never decreases).
223450 does not meet these criteria (decreasing pair of digits 50).
123789 does not meet these criteria (no double).
How many different passwords within the range given in your puzzle input meet these criteria?

Your puzzle input is 372037-905157.
"""

MIN = 372037
MAX = 905157


def _has_double(digits):
    for i in range(0, len(digits) - 1):
        if digits[i] == digits[i + 1]:
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
