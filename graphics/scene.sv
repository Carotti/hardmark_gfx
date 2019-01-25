module scene (
    input pixel_clk,
    input hsync,
    input vsync,
    input [23:0] sphere_x,
    input [23:0] sphere_y,
    input [23:0] sphere_z,
    input [23:0] sphere_radius,
    output [31:0] pixel_data
);

    import fixed_point::*;
    import vector::*;
    import graphics::*;

    wire vector_t view_ray;

    wire vector_t sphere_center;
    wire intersection_t sphere_1_intersection;

    camera main_camera (
        .pixel_clk(pixel_clk),
        .hsync(hsync),
        .vsync(vsync),
        .ray(view_ray)
    );

    sphere sphere_1 (
        .pixel_clk(pixel_clk),
        .ray(view_ray),
        .radius(sphere_radius),
        .center(sphere_center),
        .intersection(sphere_1_intersection)
    );

    assign sphere_center.x = sphere_x;
    assign sphere_center.y = sphere_y;
    assign sphere_center.z = sphere_z;

    assign pixel_data = sphere_1_intersection.intersects ? 32'hff0000ff : 32'h00000000;

endmodule