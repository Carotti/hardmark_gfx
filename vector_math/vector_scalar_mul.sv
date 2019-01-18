`define VECTOR_SCALAR_MUL(axis) \
wire axis``_overflow;\
fixed_point_mul axis``_mul (\
    .op1(scalar_op),\
    .op2(vector_op.``axis),\
    .result(result.``axis),\
    .overflow(axis``_overflow)\
)

module vector_scalar_mul
(
    input fixed_point::fixed_point_t scalar_op,
    input vector::vector_t vector_op,
    output vector::vector_t result,
    output overflow
);
    import fixed_point::*;
    import vector::*;

    `VECTOR_SCALAR_MUL(x);
    `VECTOR_SCALAR_MUL(y);
    `VECTOR_SCALAR_MUL(z);

    assign overflow = x_overflow | y_overflow | z_overflow;

endmodule