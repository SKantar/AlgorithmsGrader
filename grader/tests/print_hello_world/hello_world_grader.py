from grader import decorators

@decorators.test
@decorators.set_description("Ispisi poruku Zdravo Svete!")
@decorators.timeout(100)
def check_hello_world(m):
    if m.response != "Zdravo Svete!":
        raise Exception("Očekivana vrednost 'Zdravo Svete!', dobijena '%s'" % m.response)
