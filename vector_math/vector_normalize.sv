// Can't overflow, but answers a very inaccurate for large vectors
module vector_normalize
(
    input clk,
    input vector::vector_t op,
    output vector::vector_t result
);
    import fixed_point::*;
    import vector::*;

    

    always @(posedge clk) begin
        
    end

endmodule