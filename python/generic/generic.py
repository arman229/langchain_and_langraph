from typing import TypeVar, Generic

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self):
        self.items: list[T] = []

    def push(self, item: T):
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()
stack = Stack[int]()
stack.push(1)
# stack.push("hello")  # ❌ Type checker will give an error


print(stack.items)
