component half_adder(
    input a
    input b

    output sum
    output carry
) {
    sum = a xor b
    carry = a and b
}

component full_adder(
    input a
    input b
    input cin

    output sum
    output cout
) {
    component ha1 = half_adder(
        a = a
        b = b
    )

    component ha2 = half_adder(
        a = ha1.sum
        b = cin
    )

    sum = ha2.sum
    cout = ha1.carry or ha2.carry
}

main component simple_2bit_adder(
    input a0
    input a1
    input b0
    input b1

    output s0
    output s1
    output carry_out
) {
    component bit0 = half_adder(
        a = a0
        b = b0
    )

    component bit1 = full_adder(
        a = a1
        b = b1
        cin = bit0.carry
    )

    s0 = bit0.sum
    s1 = bit1.sum
    carry_out = bit1.cout
}