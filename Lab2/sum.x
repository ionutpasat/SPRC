struct sum {
    int x;
    int y;
};

program CHECKPROG {
    version CHECKVERS {
        int GET_SUM(sum) = 1;
    } = 1;
} = 0x31234567;