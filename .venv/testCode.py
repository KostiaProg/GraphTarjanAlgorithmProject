import tracemalloc
import time

class MemoryAndTimeTester:
    def __init__(self, func):
        self.func       = func
        self.outputs    = []
        self.times      = []
        self.memories   = []

    def test(self, args: list|dict = None):
        pos_args = [] # підготовка аргументів (не обов'язково передавати щось)
        kw_args  = {}
        if   isinstance(args, list): pos_args = args
        elif isinstance(args, dict): kw_args  = args

        tracemalloc.start() # початок підрахунків
        start = time.time()
        
        # виконання ф-ції
        result = self.func(*pos_args, **kw_args)

        fullTime = time.time() - start
        snapshot = tracemalloc.take_snapshot() # закінчення підрахунків
        peak = tracemalloc.get_traced_memory()[1] # отримання пікового значення
        tracemalloc.stop() 

        stats = snapshot.statistics('lineno') # отримання статистики по рядках кода
        memories = []
        useMemory = 0
        for stat in stats: # збереження статистики
            useMemory += stat.size
            memories.append({"size": stat.size, "count": stat.count, "average": round(stat.size/stat.count, 2)})
        
        # збереження іншийх даних
        self.memories.append({"useMemory": useMemory, "peak": peak, "stats": memories})
        self.times.append(fullTime)
        self.outputs.append(result)

    def reset(self):
        self.outputs    = []
        self.times      = []
        self.memories   = []

    def setFunc(self, func):
        self.func = func
        self.reset()

# tester.memories = [{'useMemory': (тут сума використання по рядкам ф-ції), 'peak': (пікове використання(надіюсь що пікове...)), 'stats': [{'size': (загальна кількість використано для рядка), 'count': (кількість використань), 'average': (середнє)}, ...]}]

def test():
    def something(n):
        s = sum(list(range(n)))
        return s

    tester = MemoryAndTimeTester(something)

    tester.test([10000])

    print(tester.outputs)
    print(tester.memories)
    print(tester.times)

if __name__ == "__main__":
    test()