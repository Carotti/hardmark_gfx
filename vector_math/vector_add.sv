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
    output vector::vector_t result,
    output overflow
);
    import fixed_point::*;
    import vector::*;

    `VECTOR_ADD_AXIS(x);
    `VECTOR_ADD_AXIS(y);
    `VECTOR_ADD_AXIS(z);

    assign overflow = x_overflow | y_overflow | z_overflow;

endmodule