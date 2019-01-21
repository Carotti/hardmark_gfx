module fixed_point_sub
(
    input fixed_point::fixed_point_t op1,
    input fixed_point::fixed_point_t op2,
    output fixed_point::fixed_point_t result,
    output overflow
);
    import fixed_point::*;

    wire signed [`FIXED_W-1:0] result_flatten;

    wire signed [`FIXED_W-1:0] op1_flatten;
    wire signed [`FIXED_W-1:0] op2_flatten;

    wire op1_sign;
    wire op2_sign;

    wire result_sign;

    assign op1_flatten = op1;
    assign op2_flatten = op2;

    assign result_flatten = op1_flatten - op2_flatten;

    assign result = result_flatten[`FIXED_W-1:0];

    assign op1_sign = op1_flatten < 0;
    assign op2_sign = op2_flatten < 0;

    assign result_sign = result_flatten < 0;

    assign overflow = (op1_sign != op2_sign) & (op2_sign == result_sign);

endmodule