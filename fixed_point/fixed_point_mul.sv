module fixed_point_mul
(
    input fixed_point::fixed_point_t op1,
    input fixed_point::fixed_point_t op2,
    output fixed_point::fixed_point_t result,
    output overflow
);
    import fixed_point::*;

    wire signed [(`FIXED_W*2)-1:0] result_flatten;

    wire signed [`FIXED_W-1:0] op1_flatten;
    wire signed [`FIXED_W-1:0] op2_flatten;

    wire unsigned [`FIXED_W-1:0] op1_flatten_abs;
    wire unsigned [`FIXED_W-1:0] op2_flatten_abs;

    wire op1_sign;
    wire op2_sign;

    wire result_sign;

    wire result_overflow;

    wire result_zero;

    assign op1_flatten = op1;
    assign op2_flatten = op2;

    assign op1_sign = op1_flatten < 0;
    assign op2_sign = op2_flatten < 0;

    // result_sign = ((result >> (fixed_w + fraction_w)) == bitmask(integer_w))
    // result_overflow = (result >> (fixed_w + fraction_w)) != 0 and not result_sign
    // result = (result >> fraction_w) & bitmask(fixed_w)

    assign result_sign = &result_flatten[(`FIXED_W*2)-1:`FIXED_W + `FIXED_FRACTION_W];

    // result_overflow = (result >> (fixed_w + fraction_w)) != 0 and not result_sign
    assign result_overflow = !result_sign & |result_flatten[(`FIXED_W*2)-1:`FIXED_W + `FIXED_FRACTION_W];

    assign result_zero = &(~result);

    assign op1_flatten_abs = op1_sign ? -op1_flatten : op1_flatten;
    assign op2_flatten_abs = op2_sign ? -op2_flatten : op2_flatten;

    assign result_flatten = op1_flatten * op2_flatten;

    assign result = result_flatten >> `FIXED_FRACTION_W;

    assign overflow = (((op1_sign ^ op2_sign) ^ result_sign) & ~result_zero) | result_overflow;

endmodule