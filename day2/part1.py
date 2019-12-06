input_program = '1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,13,1,19,1,5,19,23,2,10,' \
                '23,27,1,27,5,31,2,9,31,35,1,35,5,39,2,6,39,43,1,43,5,47,' \
                '2,47,10,51,2,51,6,55,1,5,55,59,2,10,59,63,1,63,6,67,2,67' \
                ',6,71,1,71,5,75,1,13,75,79,1,6,79,83,2,83,13,87,1,87,6,91' \
                ',1,10,91,95,1,95,9,99,2,99,13,103,1,103,6,107,2,107,6,111,' \
                '1,111,2,115,1,115,13,0,99,2,0,14,0'


class Processor:

    _working = 0
    memory = None

    # (handler_name, number_of_parameters)
    handlers = {
        1: ('add', 3),
        2: ('multiply', 3),
        99: ('halt', 0),
    }

    def run(self, memory):
        self._working = 1
        self.memory = memory

        instruction_pointer = 0
        while self._working:
            opcode = self.memory[instruction_pointer]

            if opcode not in self.handlers:
                raise Exception('Something went wrong')

            handler_name, number_of_parameters = self.handlers[opcode]
            handler = getattr(self, handler_name)

            parameters = self.memory[
                                   instruction_pointer + 1:
                                   instruction_pointer + number_of_parameters + 1
                                  ]
            handler(*parameters)

            instruction_pointer += number_of_parameters + 1

        return self.memory

    def add(self, x, y, z):
        self.memory[z] = self.memory[x] + self.memory[y]

    def multiply(self, x, y, z):
        self.memory[z] = self.memory[x] * self.memory[y]

    def halt(self):
        self._working = 0


def main():
    memory = list(map(int, input_program.split(',')))

    print('Initial state: {}'.format(memory))

    memory[1] = 12
    memory[2] = 2

    print('Restored state: {}'.format(memory))

    processor = Processor()
    processor.run(memory)

    print('Final state: {}'.format(memory))
    print('Position 0 value: {}'.format(memory[0]))


if __name__ == '__main__':
    main()
