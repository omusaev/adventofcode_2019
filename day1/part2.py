input_file = './input'

with open(input_file, 'r') as f:
    modules = f.readlines()

modules = [int(mass) for mass in modules]


def fuel_for_mass(mass, parts):
    fuel = mass // 3 - 2

    if fuel > 0:
        parts.append(fuel)
        fuel_for_mass(fuel, parts)

    return parts


fuel_parts_per_module = [fuel_for_mass(mass, []) for mass in modules]
total_fuel = sum([sum(parts) for parts in fuel_parts_per_module])

print('Fuel parts per module: {}'.format(fuel_parts_per_module))
print('Total fuel: {}'.format(total_fuel))
