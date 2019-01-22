`define VECTOR_ADD_AXIS(axis) \
    wire axis``_overflow;\
    fixed_point_add axis``_add (\
        .op1(op1.``axis),\
        .op2(op2.``axis),\
        .result(result.``axis),\
        .overflow(axis``_overflow)\
    )

module vector_add
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

    fixed_point_add x_add (
        .op1(op1.x),
        .op2(op2.x),
        .result(result.x),
        .overflow(x_overflow)
    );

    fixed_point_add y_add (
        .op1(op1.y),
        .op2(op2.y),
        .result(result.y),
        .overflow(y_overflow)
    );

    fixed_point_add z_add (
        .op1(op1.z),
        .op2(op2.z),
        .result(result.z),
        .overflow(z_overflow)
    );

    assign overflow = x_overflow | y_overflow | z_overflow;
    assign result = {result_x, result_y, result_z};

endmodule