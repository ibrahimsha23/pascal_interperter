import sys

INTEGER, PLUS, EOF, MINUS, WHITE_SPACE = 'INTEGER', 'PLUS', 'EOF', 'MINUS', "WHITE_SPACE"

QUIT_COMMANDS = ["quit()", "exit()"]

class Token(object):
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value
        self.next_pos_type = None
    
    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )
    def __repr__(self):
        return self.__str__()


class Interpreter(object):

    def __init__(self, text):
        self.text = text
        self.text_len = len(self.text)
        self.pos = 0
        self.current_token = None
    
    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        text = self.text.strip()

        if self.pos > self.text_len - 1:
            return Token(EOF, None)

        # get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]

        # if the character is a digit then convert it to
        # integer, create an INTEGER token, increment self.pos
        # index to point to the next character after the digit,
        # and return the INTEGER token
        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        if current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token
        
        if current_char == ' ':
            token = Token(WHITE_SPACE, current_char)
            self.pos += 1
            return token

        self.error()
    
    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def eval_next_token(self):
        if self.pos > self.text_len - 1:
            return False

        current_char = self.text[self.pos]
        if current_char.isdigit():
            return True
        elif current_char == " ":
            self.pos += 1
            return self.eval_next_token()
        return False


    def append_char(self, old_val, new_val):
        old_val = str(old_val)
        new_val = str(new_val)  
        result = old_val + new_val
        return  int(result)

    def evaluate(self):
        if self.text in QUIT_COMMANDS:
            print("Terminating the session")
            sys.exit()
        # elif self.text.startswith(QUIT_COMMANDS[0][:-2]) or self.text.startswith(QUIT_COMMANDS[1][:-2]):
        #     print("Please enter valid commands: {0} or {1}".format(QUIT_COMMANDS[0], QUIT_COMMANDS[1]))           
        import ipdb;ipdb.set_trace();

        self.current_token = self.get_next_token()

        left = self.current_token

        while self.eval_next_token():
            self.current_token = self.get_next_token()
            if self.current_token.value == " ":
                continue
            left.value = self.append_char(left.value, self.current_token.value)
            # self.pos += 1
            
        
        op = self.get_next_token()

        right = self.get_next_token()

        while self.eval_next_token():
            self.current_token = self.get_next_token()
            if self.current_token.value == " ":
                continue
            right.value = self.append_char(right.value, self.current_token.value)
            # self.pos += 1

        result = None

        if op.type == MINUS:
            result = left.value - right.value
        elif op.type == PLUS:
            result = left.value + right.value

        return result

def entry_point():
    while True:
        try:
            text = input('calc>')
            print("Text is in the format-{0}".format(text))
            interperter = Interpreter(text)
            result = interperter.evaluate()
            print(result)
        except Exception as e:
            print(e)
            print("Terminating the session, due to an error...........")
            sys.exit()

if __name__ == "__main__":
    entry_point()

