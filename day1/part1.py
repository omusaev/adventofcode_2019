input_file = './input'


def main():
    with open(input_file, 'r') as f:
        modules = f.readlines()

    total_fuel = sum([int(mass) // 3 - 2 for mass in modules])

    print('Total fuel: {}'.format(total_fuel))


if __name__ == '__main__':
    main()
