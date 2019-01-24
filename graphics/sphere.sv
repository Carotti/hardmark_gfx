module sphere
(
    input pixel_clk,
    input vector::vector_t ray, // l - Must be normalized ray coming from origin
    input vector::vector_t center, // c
    input fixed_point::fixed_point_t radius, // r
    output graphics::intersection_t intersection
);
    import fixed_point::*;
    import vector::*;
    import graphics::*;

    vector_t ray_reg;

    vector_t center_origin_reg;
    reg center_origin_overflow_reg1;
    reg center_origin_overflow_reg2;

    wire vector_t center_origin;
    wire center_origin_overflow;

    fixed_point_t dir_dot_reg;
    reg dir_dot_overflow_reg;

    wire fixed_point_t dir_dot;
    wire dir_dot_overflow;

    wire fixed_point_t dir_dot_sq;
    wire dir_dot_sq_overflow;

    fixed_point_t center_origin_mag_sq_reg;
    reg center_origin_mag_sq_overflow_reg;

    wire fixed_point_t center_origin_mag_sq;
    wire center_origin_mag_sq_overflow;

    fixed_point_t radius_sq_reg1;
    fixed_point_t radius_sq_reg2;
    reg radius_sq_overflow_reg1;
    reg radius_sq_overflow_reg2; 

    wire fixed_point_t radius_sq;
    wire radius_sq_overflow;

    wire fixed_point_t discriminant_partial;
    wire discriminant_partial_overflow;

    wire fixed_point_t discriminant;
    wire discriminant_overflow;

    wire overflow;
    wire discriminant_sign;

    // o - c
    vector_sub center_origin_sub (
        .op1(0), // Assume that the ray originated from the origin
        .op2(center),
        .result(center_origin),
        .overflow(center_origin_overflow)
    );

    // l . (o - c)
    vector_dot_product dir_vdot (
        .op1(ray_reg),
        .op2(center_origin_reg),
        .result(dir_dot),
        .overflow(dir_dot_overflow)
    );

    // (l . (o - c)) ^ 2
    fixed_point_mul dir_dot_sq_mul (
        .op1(dir_dot_reg),
        .op2(dir_dot_reg),
        .result(dir_dot_sq),
        .overflow(dir_dot_sq_overflow)
    );

    // || o - c || ^ 2
    vector_dot_product center_origin_mag_sq_vdot (
        .op1(center_origin_reg),
        .op2(center_origin_reg),
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

    // || o - c || ^ 2 - r ^ 2
    fixed_point_sub discriminant_partial_sub (
        .op1(center_origin_mag_sq),
        .op2(radius_sq_reg2),
        .result(discriminant_partial),
        .overflow(discriminant_partial_overflow)
    );

    // (l . (o - c)) ^ 2 - || o - c || ^ 2 - r ^ 2
    fixed_point_sub discriminant_sub (
        .op1(dir_dot_sq),
        .op2(discriminant_partial),
        .result(discriminant),
        .overflow(discriminant_overflow)
    );

    assign overflow = center_origin_overflow_reg2
                        | dir_dot_overflow_reg
                        | dir_dot_sq_overflow
                        | center_origin_mag_sq_overflow_reg
                        | radius_sq_overflow_reg2
                        | discriminant_partial_overflow
                        | discriminant_overflow;

    assign discriminant_sign = discriminant[`FIXED_W-1];

    always @(posedge pixel_clk) begin
        center_origin_reg <= center_origin;
        center_origin_overflow_reg1 <= center_origin_overflow;
        center_origin_overflow_reg2 <= center_origin_overflow_reg1;

        radius_sq_reg1 <= radius_sq;
        radius_sq_reg2 <= radius_sq_reg1;

        radius_sq_overflow_reg1 <= radius_sq_overflow;
        radius_sq_overflow_reg2 <= radius_sq_overflow_reg1;

        ray_reg <= ray;

        dir_dot_reg <= dir_dot;
        dir_dot_overflow_reg = dir_dot_overflow;

        center_origin_mag_sq_overflow_reg <= center_origin_mag_sq_overflow;
        center_origin_mag_sq_reg <= center_origin_mag_sq;

        intersection.intersects <= ~discriminant_sign & ~overflow;
    end

endmodule