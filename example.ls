component com(
    input a
    input b
    input c

    output x
    output y
) {
    signal s = a or c
    x = a or c
    y = b and (not c)
}

main component main(
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

    y1 = kaczka.x
    y2 = kaczka.x
}
