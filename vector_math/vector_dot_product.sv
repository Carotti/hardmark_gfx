`define VECTOR_MUL(axis) \
    wire fixed_point_t axis``_result;\
    wire axis``_overflow;\
    fixed_point_mul axis``_mul (\
        .op1(op1.``axis),\
        .op2(op2.``axis),\
        .result(axis``_result),\
        .overflow(axis``_overflow)\
    )

`define VECTOR_ADD(axis1, axis2) \
    wire fixed_point_t axis1``axis2``_result;\
    wire axis1``axis2``_overflow;\
    fixed_point_add axis1``axis2``_mul (\
        .op1(axis1``_result),\
        .op2(axis2``_result),\
        .result(axis1``axis2``_result),\
        .overflow(axis1``axis2``_overflow)\
    )

module vector_dot_product
(
    input vector::vector_t op1,
    input vector::vector_t op2,
    output fixed_point::fixed_point_t result,
    output overflow
);
    import fixed_point::*;
    import vector::*;

    `VECTOR_MUL(x);
    `VECTOR_MUL(y);
    `VECTOR_MUL(z);

    `VECTOR_ADD(x, y);
    `VECTOR_ADD(xy, z);

    assign overflow = x_overflow | y_overflow | z_overflow | xy_overflow | xyz_overflow;

    assign result = xyz_result;

endmodule