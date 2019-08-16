module test;

initial
begin
    $dumpfile("test.vcd");
    $dumpvars(0,test);
    # 10 reset = 0;
    # 513 $finish;
end

reg clk = 0;
always #1 clk = !clk;

reg reset = 1;
wire led;

Brain brain(
    .sys_clk (clk),
    .sys_rst (reset),
    .led (led)
);

endmodule