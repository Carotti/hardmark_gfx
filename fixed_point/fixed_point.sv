package fixed_point;

    `ifndef FIXED_INTEGER_W
    `define FIXED_INTEGER_W 19
    `endif

    `ifndef FIXED_FRACTION_W
    `define FIXED_FRACTION_W 13
    `endif

    typedef struct packed {
        logic [`FIXED_INTEGER_W-1:0] i;
        logic [`FIXED_FRACTION_W-1:0] f; 
    } fixed_point_t;

endpackage