

def coroutine(func):
    def wrapper(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return wrapper

class BlaBlaError(Exception):
    pass


def subgen():
    while True:
        try:
            message = yield
        except BlaBlaError:
            pass
        else:
            print('..........', message)

@coroutine
def delegator(g):
    yield from g

sub = subgen()
d = delegator(sub)
d.send('ok')
