input_file = './input'

with open(input_file, 'r') as f:
    modules = f.readlines()

total_fuel = sum([int(mass) // 3 - 2 for mass in modules])

print('Total fuel: {}'.format(total_fuel))
