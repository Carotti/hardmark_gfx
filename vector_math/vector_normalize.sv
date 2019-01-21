`timescale 1ns/1ps

// Can't overflow, but answers are very inaccurate for large vectors
module vector_normalize
(
    input clk,
    input vector::vector_t op,
    output vector::vector_t result
);
    import fixed_point::*;
    import vector::*;

    int i;
    genvar g;

    reg vector_t [`FIXED_W:0] temp_ops;

    reg fixed_point_t [`FIXED_W:0] scalars;

    wire vector_t [`FIXED_W-1:0] scalar_results;
    wire [`FIXED_W-1:0] scalar_overflow;

    wire fixed_point_t [`FIXED_W-1:0] dot_results;
    wire [`FIXED_W-1:0] dot_overflow;

    wire fixed_point_t test_bits [`FIXED_W-1:0] ;

    wire signed [`FIXED_W-1:0] [`FIXED_W-1:0] packed_dot_results;
    wire signed [`FIXED_W-1:0] one;
    wire [`FIXED_W-1:0] dot_leq_one;

    assign one = (1 << `FIXED_FRACTION_W);

    for (g = 0; g < `FIXED_W; g = g + 1) begin : gen_scalar_mul
        vector_scalar_mul smul (
            .vector_op(temp_ops[g]),
            .scalar_op(scalars[g] | test_bits[g]),
            .result(scalar_results[g]),
            .overflow(scalar_overflow[g])
        );
    end

    for (g = 0; g < `FIXED_W; g = g + 1) begin : gen_vector_dot
        vector_dot_product vdot (
            .op1(scalar_results[g]),
            .op2(scalar_results[g]),
            .result(dot_results[g]),
            .overflow(dot_overflow[g])
        );
    end

    for (g = 0; g < `FIXED_W; g = g + 1) begin : gen_leq
        assign packed_dot_results[g] = dot_results[g];
        assign dot_leq_one[g] = packed_dot_results[g] <= one;
        assign test_bits[g] = (1 << (`FIXED_W - 1 - g));
    end

    vector_scalar_mul result_smul (
        .vector_op(temp_ops[`FIXED_W]),
        .scalar_op(scalars[`FIXED_W]),
        .result(result)
    );

    always @(posedge clk) begin
        scalars[0] = '0;
        temp_ops[`FIXED_W:0] <= {temp_ops[`FIXED_W-1:0], op};
        for (i = 0; i < `FIXED_W; i = i + 1) begin
            if ((~scalar_overflow[i] & ~dot_overflow[i]) & dot_leq_one[i]) begin
                scalars[i + 1] <= scalars[i] | test_bits[i];
            end else begin
                scalars[i + 1] <= scalars[i];
            end
        end
    end

endmodule