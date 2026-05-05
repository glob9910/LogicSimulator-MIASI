component And3(
    input a
    input b
    input c

    output x
) {
    x = a and b and c
}

component Or4(
    input a
    input b
    input c
    input d

    output x
) {
    x = (a or b) or (c or d)
}

component Multiplexer(
    input I0
    input I1
    input I2
    input I3
    input S0
    input S1

    output Y
) {
    signal s0_T = S0
    signal s0_F = not S0
    signal s1_T = S1
    signal s1_F = not S1

    component g0 = And3(
        a = I0
        b = s0_F
        c = s1_F
    )
    component g1 = And3(
        a = I1
        b = s0_T
        c = s1_F
    )
    component g2 = And3(
        a = I2
        b = s0_F
        c = s1_T
    )
    component g3 = And3(
        a = I3
        b = s0_T
        c = s1_T
    )

    component final = Or4(
        a = g0.x
        b = g1.x
        c = g2.x
        d = g3.x
    )

    Y = final.x
}

main component Multi(
    input I0
    input I1
    input I2
    input I3
    input S0
    input S1

    output Y
) {
    component final = Multiplexer(
        I0 = I0
        I1 = I1
        I2 = I2
        I3 = I3
        S0 = S0
        S1 = S1
    )

    Y = final.Y
}