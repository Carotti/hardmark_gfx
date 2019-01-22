`define VECTOR_SUB_AXIS(axis) \
    wire axis``_overflow;\
    fixed_point_sub axis``_sub (\
        .op1(op1.``axis),\
        .op2(op2.``axis),\
        .result(result.``axis),\
        .overflow(axis``_overflow)\
    )

module vector_sub
(
    input vector::vector_t op1,
    input vector::vector_t op2,
    output fixed_point::fixed_point_t result,
    output overflow
);
    import fixed_point::*;
    import vector::*;

    wire x_overflow;
    wire y_overflow;
    wire z_overflow;

    fixed_point_t result_x;
    fixed_point_t result_y;
    fixed_point_t result_z;

    fixed_point_sub x_sub (
        .op1(op1.x),
        .op2(op2.x),
        .result(result_x),
        .overflow(x_overflow)
    );

    fixed_point_sub y_sub (
        .op1(op1.y),
        .op2(op2.y),
        .result(result_y),
        .overflow(y_overflow)
    );

    fixed_point_sub z_sub (
        .op1(op1.z),
        .op2(op2.z),
        .result(result_z),
        .overflow(z_overflow)
    );

    assign overflow = x_overflow | y_overflow | z_overflow;
    assign result = {result_x, result_y, result_z};

endmodule