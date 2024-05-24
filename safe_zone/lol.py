import random
import math
from typing import List, Tuple

class LOL:
    def __init__(self):
        pass

    def get_random(self) -> int:
        return random.randint(0, 100)

    def check_prime(self, num: int) -> bool:
        if num < 2:
            return False
        for i in range(2, math.isqrt(num) + 1):
            if num % i == 0:
                return False
        return True

    def generate_primes(self, n: int) -> List[int]:
        primes = []
        num = 2
        while len(primes) < n:
            if self.check_prime(num):
                primes.append(num)
            num += 1
        return primes