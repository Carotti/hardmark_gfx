module scene (
    input pixel_clk,
    output [31:0] pixel_data
);

    import fixed_point::*;
    import vector::*;
    import graphics::*;

    wire vector_t view_ray;

    wire fixed_point_t sphere_radius;
    wire vector_t sphere_center;
    wire intersection_t sphere_1_intersection;

    camera main_camera (
        .pixel_clk(pixel_clk),
        .ray(view_ray)
    );

    sphere sphere_1 (
        .ray(view_ray),
        .radius(sphere_radius),
        .center(sphere_center),
        .intersection(sphere_1_intersection)
    );

    assign sphere_radius = (1 << `FIXED_FRACTION_W);
    assign sphere_center = {32'd0, 32'd0, 32'd2 << `FIXED_FRACTION_W};

    assign pixel_data = sphere_1_intersection.intersects ? 32'hff0000ff : 32'h0;

endmodule