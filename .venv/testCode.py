import time

class TimeTester:
    def __init__(self, func):
        self.func       = func
        self.outputs    = []
        self.times      = []

    def test(self, args: list|dict = None):
        pos_args = [] # підготовка аргументів (не обов'язково передавати щось)
        kw_args  = {}
        if   isinstance(args, list): pos_args = args
        elif isinstance(args, dict): kw_args  = args

        start = time.time()
        
        result = self.func(*pos_args, **kw_args) # виконання ф-ції

        self.times.append(time.time() - start)
        self.outputs.append(result)

    def reset(self):
        self.outputs    = []
        self.times      = []

    def setFunc(self, func):
        self.func = func

def test():
    def something(n):
        s = sum(list(range(n)))
        return s

    tester = TimeTester(something)
    tester.test([10000])

    print(tester.outputs)
    print(tester.times)

if __name__ == "__main__":
    test()