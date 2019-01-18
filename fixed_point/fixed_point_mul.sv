module fixed_point_mul
(
    input fixed_point::fixed_point_t op1,
    input fixed_point::fixed_point_t op2,
    output fixed_point::fixed_point_t result,
    output overflow
);
    import fixed_point::*;

    wire signed [($bits(fixed_point_t)*2)-1:0] result_flatten;

    wire signed [$bits(fixed_point_t)-1:0] op1_flatten;
    wire signed [$bits(fixed_point_t)-1:0] op2_flatten;

    wire unsigned [$bits(fixed_point_t)-1:0] op1_flatten_abs;
    wire unsigned [$bits(fixed_point_t)-1:0] op2_flatten_abs;

    wire op1_sign;
    wire op2_sign;

    wire result_sign;

    assign op1_flatten = op1;
    assign op2_flatten = op2;

    assign op1_sign = op1_flatten < 0;
    assign op2_sign = op2_flatten < 0;

    assign result_sign = |result_flatten[($bits(fixed_point_t)*2)-1:$bits(fixed_point_t)];

    assign op1_flatten_abs = op1_sign ? -op1_flatten : op1_flatten;
    assign op2_flatten_abs = op2_sign ? -op2_flatten : op2_flatten;

    assign result_flatten = op1_flatten * op2_flatten;

    assign result = result_flatten >> `fraction_w;

    assign overflow = (op1_sign ^ op2_sign) ^ result_sign;

endmodule