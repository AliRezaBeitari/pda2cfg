import xml.etree.ElementTree as ET


class PDA:
    def __init__(self, file_name):
        self.file_name = file_name
        self.load_file()


    def load_file(self):
        tree = ET.parse(self.file_name)
        self.root = tree.getroot()
        self.parse()


    def parse(self):
        self.parse_alphabets()
        self.parse_states()
        self.parse_transitions()

    
    def parse_alphabets(self):
        alphabets_element = self.root.find('Alphabets')
        input_alphabets_element = alphabets_element.find('Input_alphabets')
        stack_alphabets_element = alphabets_element.find('Stack_alphabets')

        input_alphabets = set()
        stack_alphabets = set()
        stack_tail_letter = None

        for alphabet in input_alphabets_element:
            input_alphabets.add(alphabet.attrib['letter'])

        for alphabet in stack_alphabets_element:
            if alphabet.tag == 'alphabet':
                stack_alphabets.add(alphabet.attrib['letter'])

            elif alphabet.tag == 'tail':
                if stack_tail_letter != None:
                    raise Exception('More than one tail letter for stack!')

                else:
                    stack_tail_letter = alphabet.attrib['letter']

        if stack_tail_letter == None:
            raise Exception('No tail letter for stack!')

        self.input_alphabets = input_alphabets
        self.stack_alphabets = stack_alphabets
        self.stack_tail_letter = stack_tail_letter


    def parse_states(self):
        root_states_element = self.root.find('States')
        states_element = root_states_element.findall('state')
        initial_state_element = root_states_element.find('initialState')
        final_states_element = root_states_element.find('FinalStates')

        states = set()
        final_states = set()

        for state in states_element:
            states.add(state.attrib['name'])

        for state in final_states_element:
            final_states.add(state.attrib['name'])

        self.states = states
        self.initial_state = initial_state_element.attrib['name']
        self.final_states = final_states


    def parse_transitions(self):
        transitions_element = self.root.find('Transitions')
        transitions = []

        for transition in transitions_element:
            source = transition.attrib['source']
            destination = transition.attrib['destination']
            _input = transition.attrib['input']
            stack_read = transition.attrib['stackRead']
            stack_write = transition.attrib['stackWrite']

            transitions.append({
                'source': source,
                'destination': destination,
                'input': _input,
                'stack_read': stack_read,
                'stack_write': stack_write
            })

        self.transitions = transitions


    @staticmethod
    def lamb(inp, empty=False):
        if empty:
            return '' if inp in ('', 'lambda') else inp

        return 'λ' if inp in ('', 'lambda') else inp


    def convert_to_cfg(self):
        result_cfg = []

        for tr in self.transitions:
            # form of 5-7 (page 222 of book)
            if tr['stack_write'] in ('', 'lambda'):
                result_cfg.append('({}{}{}) → {}'.format(tr['source'], tr['stack_read'], tr['destination'], PDA.lamb(tr['input'])))

            elif len(tr['stack_write']) == 2:
                for s in self.states:
                    for bs in self.states:
                        result_cfg.append('({}{}{}) → {}({}{}{})({}{}{})'.format(
                            tr['source'],
                            tr['stack_read'],
                            s,
                            PDA.lamb(tr['input'], True),
                            self.initial_state,
                            tr['stack_write'][0],
                            bs,
                            bs,
                            tr['stack_write'][1],
                            s
                        ))

            else:
                raise Exception('Stack write should be 0 length or 2: "{}"'.format(tr['stack_write']))

        return result_cfg