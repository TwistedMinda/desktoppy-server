C:/Users/Julien/projects/ai/script.py:

import random
import string

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

poem = """
The moon's soft glow, a beacon bright,
A midnight sky, where stars take flight.
The world is hushed, in quiet sleep,
As I stand here, my heart does creep.

In this still night, I find my peace,
A sense of calm, the world to cease.
The moon's pale light, upon me shines,
And all my worries, like clouds, decline.

But then the dawn, begins its rise,
And with it, my peaceful sighs.
The sun's warm touch, on my face so fair,
Awakens life, and banishes despair.

"""

print(poem)