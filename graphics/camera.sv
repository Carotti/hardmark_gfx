module camera
(
    input pixel_clk,
    output vector::vector_t ray
);
    parameter hWidth = 1024;
    parameter hFrontPorch = 24;
    parameter hBackPorch = 160;
    parameter hSyncWidth = 136;
    
    parameter vWidth = 768;
    parameter vFrontPorch = 9;
    parameter vBackPorch = 23;
    parameter vSyncWidth = 6;

    parameter fov_shift = 1;

    import fixed_point::*;
    import vector::*;

    reg [$clog2(hWidth + hFrontPorch + hSyncWidth + hBackPorch) - 1:0] hCount;
    reg [$clog2(vWidth + vFrontPorch + vSyncWidth + vBackPorch) - 1:0] vCount;

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

    assign unnormalized_ray.x = (hCount - hWidth / 2) << fov_shift;
    assign unnormalized_ray.y = (vWidth / 2 - vCount) << fov_shift;
    assign unnormalized_ray.z = 1;

    initial hCount = 0;
    initial vCount = 0;

    always @(posedge pixel_clk) begin
        hCount <= hReset ? 0 : hCount + 1;
        vCount <= hReset ? (vReset ? 0 : vCount + 1) : vCount;
    end

endmodule