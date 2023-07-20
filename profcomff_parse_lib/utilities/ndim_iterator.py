class NDimIterator:
    """
    Код:
        iterator = NDimIterator(3, 2)
        for iters in iterator:
            print(iters)
    Выдаст:
        [0, 0, 0]
        [0, 0, 1]
        [0, 1, 0]
        [0, 1, 1]
        [1, 0, 0]
        [1, 0, 1]
        [1, 1, 0]
        [1, 1, 1]
    """

    def __init__(self, dim, max_value):
        """
        :param dim: Размерность.
        :param max_value: Максимальное число у одной оси.
        """
        self.dim = dim
        self.max_value = max_value

    def __iter__(self):
        self.iters = [0] * self.dim
        self.iters[-1] -= 1
        return self

    def __next__(self):
        if sum(self.iters) == self.dim * (self.max_value - 1):
            raise StopIteration

        self._add_value(self.dim - 1)
        return self.iters

    def _add_value(self, index):
        self.iters[index] += 1
        if self.iters[index] == self.max_value:
            self.iters[index] = 0
            self._add_value(index - 1)


if __name__ == "__main__":
    iterator = NDimIterator(3, 2)
    for iters in iterator:
        print(iters)
