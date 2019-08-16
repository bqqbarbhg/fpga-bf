from migen import *
from migen.fhdl import verilog
import os

program = '++>><<H      '
ops = ' +-><H'

code = [ops.index(c) for c in program]

class BrainFpga(Module):
    def __init__(self):
        self.led = Signal()
        self.ip = Signal(8)
        self.ptr = Signal(10)
        self.next_ptr = Signal(self.ptr.nbits)
        self.phase = Signal()
        self.value = Signal(8)
        self.result = Signal(8)
        self.halt = Signal()
        self.aluop = Signal(2)

        self.op = Signal(4)

        self.specials.mem_code = Memory(4, len(ops), init=code)
        self.specials.mem_data = Memory(8, 1024, init=[0]*1024)

        self.specials.rd_code = self.mem_code.get_port()
        self.specials.rw_data = self.mem_data.get_port(write_capable=True)
        self.specials += [self.rd_code, self.rw_data]

        # Toggle phase every clock
        self.sync += self.phase.eq(self.phase + 1)

        # Read `mem_code` at `ip`
        self.comb += [
            self.rd_code.adr.eq(self.ip),
            self.op.eq(self.rd_code.dat_r),
        ]

        # Read `mem_data` at `ptr`
        self.comb += [
            self.rw_data.adr.eq(self.ptr),
        ]

        # Always write in the second phase
        self.comb += self.rw_data.we.eq(self.phase)

        self.comb += self.aluop.eq(Array([0,1,2,0])[self.op])

        self.comb += self.value.eq(self.rw_data.dat_r)

        self.comb += self.result.eq(Array([
            self.value,
            self.value + 1,
            self.value - 1,
        ])[self.aluop])

        self.comb += If(self.op == 3,
            self.next_ptr.eq(self.ptr + 1),
        ).Elif(self.op == 4,
            self.next_ptr.eq(self.ptr - 1),
        ).Else(
            self.next_ptr.eq(self.ptr),
        )

        self.comb += self.halt.eq(self.op == 5)
        self.comb += self.rw_data.dat_w.eq(self.result),

        self.sync += If(self.phase == 1,
            self.ip.eq(self.ip + (self.halt^1)),
            self.ptr.eq(self.next_ptr)
        )

        self.comb += self.led.eq(self.value > 0)

        self.ios = { self.led }

if __name__ == '__main__':
    os.makedirs('build', exist_ok=True)
    os.chdir('build')
    brain = BrainFpga()
    verilog.convert(brain, brain.ios, 'Brain').write('brain.v')