module sphere
(
    input vector::vector_t view_origin, // o
    input vector::vector_t view_direction, // l - Must be normalized
    input vector::vector_t center, // c
    input fixed_point::fixed_point_t radius, // r
    output graphics::intersection_t intersection
);
    import fixed_point::*;
    import vector::*;
    import graphics::*;

    wire vector_t center_origin;
    wire center_origin_overflow;

    wire fixed_point_t dir_dot;
    wire dir_dot_overflow;

    wire fixed_point_t dir_dot_sq;
    wire dir_dot_sq_overflow;

    wire fixed_point_t center_origin_mag_sq;
    wire center_origin_mag_sq_overflow;

    wire fixed_point_t radius_sq;
    wire radius_sq_overflow;

    wire fixed_point_t discriminant_partial;
    wire discriminant_partial_overflow;

    wire fixed_point_t discriminant;
    wire discriminant_overflow;

    wire overflow;

    // o - c
    vector_sub center_origin_sub (
        .op1(view_origin),
        .op2(center),
        .result(center_origin),
        .overflow(center_origin_overflow)
    );

    // l . (o - c)
    vector_dot_product dir_vdot (
        .op1(view_direction),
        .op2(center_origin),
        .result(dir_dot),
        .overflow(dir_dot_overflow)
    );

    // (l . (o - c)) ^ 2
    fixed_point_mul dir_dot_sq_mul (
        .op1(dir_dot),
        .op2(dir_dot),
        .result(dir_dot_sq),
        .overflow(dir_dot_sq_overflow)
    );

    // || o - c || ^ 2
    vector_dot_product center_origin_mag_sq_vdot (
        .op1(center_origin),
        .op2(center_origin),
        .result(center_origin_mag_sq),
        .overflow(center_origin_mag_sq_overflow)
    );

    // r ^ 2
    fixed_point_mul radius_sq_mul (
        .op1(radius),
        .op2(radius),
        .result(radius_sq),
        .overflow(radius_sq_overflow)
    );

    // (l . (o - c)) ^ 2 - || o - c || ^ 2
    fixed_point_sub discriminant_partial_sub (
        .op1(dir_dot_sq),
        .op2(center_origin_mag_sq),
        .result(discriminant_partial),
        .overflow(discriminant_partial_overflow)
    );

    // (l . (o - c)) ^ 2 - || o - c || ^ 2 - r ^ 2
    fixed_point_sub discriminant_sub (
        .op1(discriminant_partial),
        .op2(radius_sq),
        .result(discriminant),
        .overflow(discriminant_overflow)
    );

    assign overflow = center_origin_overflow 
                        | dir_dot_overflow
                        | dir_dot_sq_overflow
                        | center_origin_mag_sq_overflow
                        | radius_sq_overflow
                        | discriminant_partial_overflow
                        | discriminant_overflow;

    assign intersection.intersects = (discriminant >= 0) & ~overflow;

endmodule