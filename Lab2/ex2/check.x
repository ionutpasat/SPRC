struct student {
    string nume<>;
    string grupa<>;
};

program CHECKPROG {
    version CHECKVERS {
        string GRADE(student) = 1;
    } = 1;
} = 0x31234567;