from itertools import product

from part1 import Processor, input_program


def main():
    initial_memory = list(map(int, input_program.split(',')))

    needle = 19690720
    processor = Processor()

    found_noun, found_verb = None, None
    for noun, verb in product(range(0, 100), range(0, 100)):
        memory = list(initial_memory)

        memory[1] = noun
        memory[2] = verb

        processor.run(memory)

        result = memory[0]

        if result == needle:
            found_noun = noun
            found_verb = verb
            break
    else:
        print('Have not found the right combination')
        exit(1)

    print('Noun, verb: {}, {}'.format(found_noun, found_verb))

    answer = 100 * found_noun + found_verb

    print('Answer: {}'.format(answer))


if __name__ == '__main__':
    main()
