module fixed_point_add
(
    input fixed_point::fixed_point_t op1,
    input fixed_point::fixed_point_t op2,
    output fixed_point::fixed_point_t result,
    output overflow
);
    import fixed_point::*;

    wire [$bits(fixed_point_t):0] result_flatten;

    wire [$bits(fixed_point_t)-1:0] op1_flatten;
    wire [$bits(fixed_point_t)-1:0] op2_flatten;

    assign op1_flatten = op1;
    assign op2_flatten = op2;

    assign result_flatten = op1_flatten + op2_flatten;

    assign overflow = result_flatten[$bits(fixed_point_t)];
    assign result = result_flatten[$bits(fixed_point_t)-1:0];

endmodule