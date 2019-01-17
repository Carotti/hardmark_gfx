package fixed_point;

    `define integer_w 19
    `define fraction_w 13

    typedef struct packed {
        logic [`integer_w-1:0] i;
        logic [`fraction_w-1:0] f; 
    } fixed_point_t;

endpackage