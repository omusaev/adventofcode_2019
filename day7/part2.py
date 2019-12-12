from itertools import permutations

input_program = '3,8,1001,8,10,8,105,1,0,0,21,34,47,72,81,94,175,256,337,418,99999,3,9,102,3,9,9,1001,9,3,9,4,9,99,3,9,101,4,9,9,1002,9,5,9,4,9,99,3,9,1001,9,5,9,1002,9,5,9,1001,9,2,9,1002,9,5,9,101,5,9,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,1001,9,4,9,102,4,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99'


class Processor:

    _working = 0
    _instruction_pointer = None
    _last_interruption = None
    memory = None
    input_stream = None
    output_stream = None

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

    class Interruptions:
        HALTED = 1
        WAITING_FOR_INPUT = 2

    def __init__(self, memory):
        self.memory = memory
        self._instruction_pointer = 0

    def run(self, input_stream, output_stream):
        self._working = 1
        self.input_stream = input_stream
        self.output_stream = output_stream

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

            # [1,2,3], [a, b, c] -> [(1,a), (2,b), (3,c)]
            shift_instruction_pointer = handler(*list(zip(modes, parameters)))

            if shift_instruction_pointer is not False:
                self._instruction_pointer += number_of_parameters + 1

        return self._last_interruption

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
        self._last_interruption = self.Interruptions.HALTED

    def input(self, z):
        try:
            x = int(self.input_stream.pop(0))
        except IndexError:
            self._working = 0
            self._last_interruption = self.Interruptions.WAITING_FOR_INPUT
            return False

        self._write_value(x, z)

    def output(self, x):
        x_v = self._get_value(x)
        self.output_stream.append(x_v)

    def jump_if_true(self, x, y):
        x_v = self._get_value(x)
        y_v = self._get_value(y)

        if x_v:
            self._instruction_pointer = y_v
            return False

    def jump_if_false(self, x, y):
        x_v = self._get_value(x)
        y_v = self._get_value(y)

        if not x_v:
            self._instruction_pointer = y_v
            return False

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
    amplifier_controller_software = list(map(int, input_program.split(',')))
    possible_phase_settings = [5, 6, 7, 8, 9]
    number_of_amplifiers = len(possible_phase_settings)

    thruster_signals = []
    for phase_settings_combination in permutations(possible_phase_settings):

        amplifiers = []
        predefined_inputs = []
        for i, phase_setting in zip(range(number_of_amplifiers), phase_settings_combination):
            amplifiers.append(Processor(list(amplifier_controller_software)))

            if i == 0:
                predefined_inputs.append([phase_setting, 0])
            else:
                predefined_inputs.append([phase_setting])

        halted = False
        prev_output_stream = []
        while not halted:
            for amplifier in amplifiers:
                input_stream = []
                if predefined_inputs:
                    input_stream = predefined_inputs.pop(0)

                input_stream += list(prev_output_stream)

                current_output_stream = []
                interruption = amplifier.run(input_stream, current_output_stream)

                if interruption == Processor.Interruptions.HALTED:
                    halted = True

                prev_output_stream = current_output_stream

        thruster_signals.append(next(iter(prev_output_stream)))

    max_thruster_signal = max(thruster_signals)
    print('Max thruster signal: {}'.format(max_thruster_signal))


if __name__ == '__main__':
    main()
