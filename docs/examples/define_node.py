import asyncio

from src.core.node import Node


class A(Node):
    async def execute(self):
        await asyncio.sleep(1)
        input_data = self.node_context.input_data
        print(self.name)
        return f"{input_data} processed by A"


class B(Node):
    async def execute(self):
        await asyncio.sleep(1)
        input_data = self.node_context.input_data
        print(self.name)
        return f"{input_data} processed by B"


class C(Node):
    async def execute(self):
        await asyncio.sleep(1)
        input_data = self.node_context.input_data
        # a = 1/0
        print(self.name)
        return f"{input_data} processed by C"


class D(Node):
    async def execute(self):
        await asyncio.sleep(1)
        input_data = self.node_context.input_data
        print(self.name)
        return f"{input_data} processed by D"


class E(Node):
    async def execute(self):
        await asyncio.sleep(1)
        input_data = self.node_context.input_data
        print(self.name)
        return f"{input_data} processed by E"


class F(Node):
    async def execute(self):
        await asyncio.sleep(1)
        input_data = self.node_context.input_data
        print(self.name)
        return f"{input_data} processed by F"


class G(Node):
    async def execute(self):
        await asyncio.sleep(1)
        input_data = self.node_context.input_data
        print(self.name)
        return f"{input_data} processed by G"


class H(Node):
    async def execute(self):
        await asyncio.sleep(1)
        input_data = self.node_context.input_data
        print(self.name)
        return f"{input_data} processed by H"


node_a = A({"data": "start"})
node_b = B()
node_c = C()
node_d = D()
node_e = E()
node_f = F()
node_g = G()
node_h = H()