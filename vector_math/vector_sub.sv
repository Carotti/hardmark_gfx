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
    output vector::vector_t result,
    output overflow
);
    import fixed_point::*;
    import vector::*;

    `VECTOR_SUB_AXIS(x);
    `VECTOR_SUB_AXIS(y);
    `VECTOR_SUB_AXIS(z);

    assign overflow = x_overflow | y_overflow | z_overflow;

endmodule