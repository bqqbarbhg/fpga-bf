
module top (
    input CLK,
    output LED,
    output USBPU
);

    assign USBPU = 0;

    reg [5:0] reset_count = 0;
    wire nreset = &reset_count;
    always @(posedge CLK) begin
        reset_count <= reset_count + !nreset;
    end

    Brain brain(
        .sys_clk (CLK),
        .sys_rst (!nreset),
        .led (LED)
    );

endmodule
