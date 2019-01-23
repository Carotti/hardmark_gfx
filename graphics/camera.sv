module camera
(
    input pixel_clk,
    output vector::vector_t ray
);
    parameter hWidth = 1680;
    parameter hFrontPorch = 48;
    parameter hBackPorch = 80;
    parameter hSyncWidth = 32;
    
    parameter vWidth = 1050;
    parameter vFrontPorch = 3;
    parameter vBackPorch = 21;
    parameter vSyncWidth = 6;

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

    // 5 Makes the normalization accuracy pretty good
    assign unnormalized_ray.x = (hCount - hWidth / 2) << 5;
    assign unnormalized_ray.y = (vWidth / 2 - vCount) << 5;
    assign unnormalized_ray.z = 24'h4000; // Fixed point 2

    initial hCount = 0;
    initial vCount = 0;

    always @(posedge pixel_clk) begin
        hCount <= hReset ? 0 : hCount + 1;
        vCount <= hReset ? (vReset ? 0 : vCount + 1) : vCount;
    end

endmodule