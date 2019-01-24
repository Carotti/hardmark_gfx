`timescale 1ns/1ps

// Since the sign bit will be set, we can remove one pipeline stage
`define PIPELINE_STAGES (`FIXED_W - 1)

// Can't overflow, but answers are very inaccurate for large vectors
module vector_normalize
(
    input clk,
    input vector::vector_t op,
    output vector::vector_t result
);
    import fixed_point::*;
    import vector::*;

    initial
    begin
        $dumpfile("test.vcd");
        $dumpvars(0,vector_normalize);
    end

    int i;
    genvar g;

    vector_t [`PIPELINE_STAGES:0] temp_ops_reg;
    vector_t [`PIPELINE_STAGES:0] temp_ops;
    fixed_point_t [`PIPELINE_STAGES:0] scalars_reg;
    fixed_point_t [`PIPELINE_STAGES:0] scalars;

    vector_t [`PIPELINE_STAGES:0] scalar_results_reg;
    reg [`PIPELINE_STAGES:0] scalar_overflow_reg;

    wire vector_t [`PIPELINE_STAGES:0] scalar_results;
    wire [`PIPELINE_STAGES:0] scalar_overflow;

    // Don't care about the dot product in the final pipeline stage
    // It should be 1 (or at least very close to 1)
    wire fixed_point_t [`PIPELINE_STAGES-1:0] dot_results;
    wire [`PIPELINE_STAGES-1:0] dot_overflow;
    wire signed [`FIXED_W-1:0] [`PIPELINE_STAGES-1:0] packed_dot_results;
    wire [`PIPELINE_STAGES-1:0] dot_leq_one;

    wire fixed_point_t one;

    wire fixed_point_t test_bits [`PIPELINE_STAGES:0];

    // Test bit of the final pipeline stage is always 0
    assign test_bits[`PIPELINE_STAGES] = 0;

    assign one = (1 << `FIXED_FRACTION_W);

    for (g = 0; g <= `PIPELINE_STAGES; g = g + 1) begin : gen_scalar_mul
        vector_scalar_mul smul (
            .vector_op(temp_ops[g]),
            .scalar_op(scalars[g] | test_bits[g]),
            .result(scalar_results[g]),
            .overflow(scalar_overflow[g])
        );
    end

    for (g = 0; g < `PIPELINE_STAGES; g = g + 1) begin : gen_vector_dot
        vector_dot_product vdot (
            .op1(scalar_results_reg[g]),
            .op2(scalar_results_reg[g]),
            .result(dot_results[g]),
            .overflow(dot_overflow[g])
        );
    end

    for (g = 0; g < `PIPELINE_STAGES; g = g + 1) begin : gen_leq
        assign packed_dot_results[g] = dot_results[g];
        assign dot_leq_one[g] = packed_dot_results[g] <= one;
        assign test_bits[g] = (1 << (`PIPELINE_STAGES - 1 - g));
    end

    initial scalars[0] = '0;

    always @(posedge clk) begin
        temp_ops[0] <= op;
        for (i = 0; i < `PIPELINE_STAGES; i = i + 1) begin
            temp_ops_reg[i] <= temp_ops[i];
            temp_ops[i + 1] <= temp_ops_reg[i];

            scalar_results_reg[i] <= scalar_results[i];
            scalar_overflow_reg[i] <= scalar_overflow[i];

            scalars_reg[i] <= scalars[i];

            if ((~scalar_overflow_reg[i] & ~dot_overflow[i]) & dot_leq_one[i]) begin
                scalars[i + 1] <= scalars_reg[i] | test_bits[i];
            end else begin
                scalars[i + 1] <= scalars_reg[i];
            end
        end
        result <= scalar_results[`PIPELINE_STAGES];
    end

endmodule