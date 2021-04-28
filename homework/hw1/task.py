class Permutator:
    def __init__(self):
        self.all_permutations = []

    def make_permutations(self, n):
        self.permutation([i for i in range(n)], 0)
        print("\n".join(sorted(self.all_permutations)))

    def permutation(self, li, index):
        if len(li) == index + 1:
            self.all_permutations.append(" ".join(list(map(lambda x: str(x), li))))
        for i in range(index, len(li)):
            li[index], li[i] = li[i], li[index]
            self.permutation(li, index + 1)
            li[index], li[i] = li[i], li[index]


print("Input number between 1 and 7 ( 1 <= n <= 7)")

a = int(input())

p = Permutator()
print("All permutations: ")
p.make_permutations(a)
