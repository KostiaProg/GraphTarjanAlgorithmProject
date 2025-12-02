import tracemalloc
import time

class MemoryAndTimeTester:
    def __init__(self, func):
        self.func       = func
        self.outputs    = []
        self.times      = []
        self.memoryes   = []

    def test(self, args : list|dict = None):
        pos_args = [] # підготовка аргументів
        kw_args  = {}
        if   isinstance(args, list): pos_args = args
        elif isinstance(args, dict): kw_args  = args

        tracemalloc.start()
        start = time.time()
        
        # виконання ф-ції
        result = self.func(*pos_args, **kw_args)

        fulTime = time.time() - start
        snapshot = tracemalloc.take_snapshot()
        peak = tracemalloc.get_traced_memory()[1]
        tracemalloc.stop()

        stats = snapshot.statistics('lineno')
        memoryes = []
        useMemory = 0
        for stat in stats:
            useMemory += stat.size
            memoryes.append({"size": stat.size, "count": stat.count, "average": round(stat.size/stat.count, 2)})
        
        self.memoryes.append({"useMemory": useMemory, "peak": peak, "stats": memoryes})
        self.times.append(fulTime)
        self.outputs.append(result)

# tester.memoryes = [{'useMemory': (тут сума використання по рядкам ф-ції), 'peak': (пікове використання(надіюсь що пікове...)), 'stats': [{'size': (загальна кількість використано для рядка), 'count': (кількість використань), 'average': (середнє)}, ...]}]

def something(n):
    s = sum(list(range(n)))
    return s

tester = MemoryAndTimeTester(something)

tester.test([10000])

print(tester.outputs)
print(tester.memoryes)
print(tester.times)