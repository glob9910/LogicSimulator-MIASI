component compare(
    input a
    input b

    output eq
    output gt
    output lt
) {
    eq = a xnor b
    gt = a and not b
    lt = not a and b 
}

component and3(
    input a
    input b
    input c

    output x
) {
    x = a and b and c
}

component and4(
    input a
    input b
    input c
    input d

    output x
) {
    x = (a and b) and (c and d)
}

component or4(
    input a
    input b
    input c
    input d

    output x
) {
    x = (a or b) or (c or d)
}

component Comparator(
    input A0
    input A1
    input A2
    input A3
    input B0
    input B1
    input B2
    input B3

    output eq
    output gt
    output lt
) {
    component c0 = compare(a = A0 b = B0)
    component c1 = compare(a = A1 b = B1)
    component c2 = compare(a = A2 b = B2)
    component c3 = compare(a = A3 b = B3)

    component equal = and4(a = c0.eq b = c1.eq c = c2.eq d = c3.eq)

    signal g3 = c3.gt
    signal g2 = c3.eq and c2.gt
    component g1 = and3(a = c3.eq b = c2.eq c = c1.gt)
    component g0 = and4(a = c3.eq b = c2.eq c = c1.eq d = c0.gt)
    component greater = or4(a = g3 b = g2 c = g1.x d = g0.x)

    signal l3 = c3.lt
    signal l2 = c3.eq and c2.lt
    component l1 = and3(a = c3.eq b = c2.eq c = c1.lt)
    component l0 = and4(a = c3.eq b = c2.eq c = c1.eq d = c0.lt)
    component less = or4(a = l3 b = l2 c = l1.x d = l0.x)

    eq = equal.x
    gt = greater.x
    lt = less.x
}

main component Main(
    input A0
    input A1
    input A2
    input A3
    input B0
    input B1
    input B2
    input B3

    output eq
    output gt
    output lt
) {
    component compare4 = Comparator(
        A0 = A0
        A1 = A1
        A2 = A2
        A3 = A3
        B0 = B0
        B1 = B1
        B2 = B2
        B3 = B3
    )

    eq = compare4.eq
    gt = compare4.gt
    lt = compare4.lt
}