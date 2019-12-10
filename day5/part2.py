input_program = '3,225,1,225,6,6,1100,1,238,225,104,0,1102,91,92,225,1102,85,13,225,1,47,17,224,101,-176,224,224,4,224,1002,223,8,223,1001,224,7,224,1,223,224,223,1102,79,43,225,1102,91,79,225,1101,94,61,225,1002,99,42,224,1001,224,-1890,224,4,224,1002,223,8,223,1001,224,6,224,1,224,223,223,102,77,52,224,1001,224,-4697,224,4,224,102,8,223,223,1001,224,7,224,1,224,223,223,1101,45,47,225,1001,43,93,224,1001,224,-172,224,4,224,102,8,223,223,1001,224,1,224,1,224,223,223,1102,53,88,225,1101,64,75,225,2,14,129,224,101,-5888,224,224,4,224,102,8,223,223,101,6,224,224,1,223,224,223,101,60,126,224,101,-148,224,224,4,224,1002,223,8,223,1001,224,2,224,1,224,223,223,1102,82,56,224,1001,224,-4592,224,4,224,1002,223,8,223,101,4,224,224,1,224,223,223,1101,22,82,224,1001,224,-104,224,4,224,1002,223,8,223,101,4,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,8,226,677,224,102,2,223,223,1005,224,329,1001,223,1,223,1007,226,226,224,1002,223,2,223,1006,224,344,101,1,223,223,108,226,226,224,1002,223,2,223,1006,224,359,1001,223,1,223,107,226,677,224,102,2,223,223,1006,224,374,101,1,223,223,8,677,677,224,102,2,223,223,1006,224,389,1001,223,1,223,1008,226,677,224,1002,223,2,223,1006,224,404,101,1,223,223,7,677,677,224,1002,223,2,223,1005,224,419,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,434,101,1,223,223,1108,226,226,224,102,2,223,223,1005,224,449,1001,223,1,223,107,226,226,224,102,2,223,223,1005,224,464,101,1,223,223,1007,677,677,224,102,2,223,223,1006,224,479,101,1,223,223,1007,226,677,224,102,2,223,223,1005,224,494,1001,223,1,223,1008,226,226,224,1002,223,2,223,1005,224,509,1001,223,1,223,1108,677,226,224,1002,223,2,223,1006,224,524,1001,223,1,223,108,677,677,224,1002,223,2,223,1005,224,539,101,1,223,223,108,226,677,224,1002,223,2,223,1005,224,554,101,1,223,223,1008,677,677,224,1002,223,2,223,1006,224,569,1001,223,1,223,1107,677,677,224,102,2,223,223,1005,224,584,1001,223,1,223,7,677,226,224,102,2,223,223,1005,224,599,1001,223,1,223,8,677,226,224,1002,223,2,223,1005,224,614,1001,223,1,223,7,226,677,224,1002,223,2,223,1006,224,629,101,1,223,223,1107,677,226,224,1002,223,2,223,1005,224,644,1001,223,1,223,1107,226,677,224,102,2,223,223,1006,224,659,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,674,101,1,223,223,4,223,99,226'


class Processor:

    _working = 0
    _instruction_pointer = None
    memory = None

    # (handler_name, number_of_parameters)
    handlers = {
        1: ('add', 3),
        2: ('multiply', 3),
        3: ('input', 1),
        4: ('output', 1),
        5: ('jump_if_true', 2),
        6: ('jump_if_false', 2),
        7: ('less_than', 3),
        8: ('equals', 3),
        99: ('halt', 0),
    }

    BY_REFERENCE = '0'
    BY_VALUE = '1'

    def run(self, memory):
        self._working = 1
        self.memory = memory
        self._instruction_pointer = 0

        while self._working:
            modes_and_opcode = str(self.memory[self._instruction_pointer])
            # "1102" -> "02"; "02" -> 2
            opcode = int(modes_and_opcode[-2:])

            if opcode not in self.handlers:
                raise Exception('Something went wrong')

            handler_name, number_of_parameters = self.handlers[opcode]
            handler = getattr(self, handler_name)

            # "11" -> 11 -> "011" -> "110"
            modes = str(int(modes_and_opcode[:-2] or '0')).zfill(number_of_parameters)[::-1]

            parameters = self.memory[
                                   self._instruction_pointer + 1:
                                   self._instruction_pointer + number_of_parameters + 1
                                  ]

            self._instruction_pointer += number_of_parameters + 1
            # [1,2,3], [a, b, c] -> [(1,a), (2,b), (3,c)]
            handler(*list(zip(modes, parameters)))

        return self.memory

    def _get_value(self, x):
        mode = x[0]
        if mode == self.BY_REFERENCE:
            return self.memory[x[1]]
        elif mode == self.BY_VALUE:
            return x[1]

    def _write_value(self, x, z):
        if z[0] != self.BY_REFERENCE:
            raise Exception('Wrong address mode')

        self.memory[z[1]] = x

    def add(self, x, y, z):
        x_v = self._get_value(x)
        y_v = self._get_value(y)
        self._write_value(x_v + y_v, z)

    def multiply(self, x, y, z):
        x_v = self._get_value(x)
        y_v = self._get_value(y)
        self._write_value(x_v * y_v, z)

    def halt(self):
        self._working = 0

    def input(self, z):
        x = int(input('Enter: '))
        self._write_value(x, z)

    def output(self, x):
        x_v = self._get_value(x)
        print('Output: {}'.format(x_v))

    def jump_if_true(self, x, y):
        x_v = self._get_value(x)
        y_v = self._get_value(y)

        if x_v:
            self._instruction_pointer = y_v

    def jump_if_false(self, x, y):
        x_v = self._get_value(x)
        y_v = self._get_value(y)

        if not x_v:
            self._instruction_pointer = y_v

    def less_than(self, x, y, z):
        x_v = self._get_value(x)
        y_v = self._get_value(y)

        result = 1 if x_v < y_v else 0

        self._write_value(result, z)

    def equals(self, x, y, z):
        x_v = self._get_value(x)
        y_v = self._get_value(y)

        result = 1 if x_v == y_v else 0

        self._write_value(result, z)


def main():
    memory = list(map(int, input_program.split(',')))

    processor = Processor()
    processor.run(memory)


if __name__ == '__main__':
    main()
