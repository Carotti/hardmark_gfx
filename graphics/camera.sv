module camera
(
    input pixel_clk,
    input hsync,
    input vsync,
    output vector::vector_t ray,
    output [10:0] hcount,
    output [10:0] vcount
);
    parameter hWidth = 1280;
    parameter hFrontPorch = 72;
    parameter hBackPorch = 216;
    parameter hSyncWidth = 80;
    
    parameter vWidth = 720;
    parameter vFrontPorch = 3;
    parameter vBackPorch = 22;
    parameter vSyncWidth = 5;

    import fixed_point::*;
    import vector::*;

    reg [$clog2(hWidth + hFrontPorch + hSyncWidth + hBackPorch) - 1:0] hCount;
    reg [$clog2(vWidth + vFrontPorch + vSyncWidth + vBackPorch) - 1:0] vCount;
    
    assign hcount = hCount;
    assign vcount = vCount;

    wire hReset;
    wire vReset;

    wire vector_t unnormalized_ray;

    vector_normalize vnorm (
        .clk(pixel_clk),
        .op(unnormalized_ray),
        .result(ray)
    );

    assign hReset = (hCount == hWidth + hFrontPorch + hSyncWidth + hBackPorch - 1);
    assign vReset = (vCount == vWidth + vFrontPorch + vSyncWidth + vBackPorch - 1);

    // 5 Makes the normalization accuracy pretty good
    assign unnormalized_ray.x = (hCount - hWidth / 2) << 5;
    assign unnormalized_ray.y = (vWidth / 2 - vCount) << 5;
    assign unnormalized_ray.z = 24'h4000; // Fixed point 2

    initial hCount = 0;
    initial vCount = 0;

    reg hsync_old;
    reg vsync_old;

    always @(posedge pixel_clk) begin
        if (~hsync_old & hsync) begin
            hCount <= hWidth + hFrontPorch;
        end else begin
            hCount <= hReset ? 0 : hCount + 1;
        end

        if (~vsync_old & vsync) begin
            vCount <= vWidth + vFrontPorch;
        end else begin
            vCount <= hReset ? (vReset ? 0 : vCount + 1) : vCount;
        end

        hsync_old = hsync;
        vsync_old = vsync;
    end

endmodule