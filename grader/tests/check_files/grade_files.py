from grader import decorators

@decorators.test
@decorators.set_description("Upisi poruku Zdravo Svete! u datoteku 'output.txt'")
@decorators.timeout(100)
def check_hello_world(m):
    with open('output.txt') as f:
        s = f.read()
        if s != "Zdravo Svete!":
            raise Exception("Očekivana vrednost 'Zdravo Svete!', dobijena '%s'" % s)

