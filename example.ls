component com(
    input a
    input b
    input c

    output x
    output y
) {
    signal s = a or c
    x = s
    y = b and (not c)
}

component krowa(
    input a
    input b
    output c
) {
    c = a xor b or not a
}

main component my_circuit(
    input x1
    input x2

    output y1
    output y2
) {
    component kaczka = com(
        a = x1
        b = 1
        c = x1 or x2
    )

    component kura = krowa(
        a = x1
        b = kaczka.a
    )

    y1 = kaczka.x
    y2 = kura.c
}
