def fact_rec(n):
    if n == 0:
        return 1
    else:
        return n * fact_rec(n-1)


def fact_cps(n, cont):
    if n == 0:
        return cont(1)
    else:
        return fact_cps(n-1, lambda value: cont(n * value))


def end_cont(n):
    return n


def trampoline(f, *args):
    v = f(*args)
    while callable(v):
        v = v()
    return v


def fact_cps_thunked(n, cont):
    if n == 0:
        return cont(1)
    else:
        return lambda: fact_cps_thunked(
            n - 1,
            lambda value: lambda: cont(n * value))


def fib_rec(n):
    if n <= 2:
        return 1
    else:
        return fib_rec(n-1) + fib_rec(n-2)


def fib_cps(n, cont):
    if n <= 2:
        return cont(1)
    else:
        return fact_cps(
            n-1,
            lambda value1: fib_cps(
                n-2,
                lambda value2: cont(value1 + value2)
            )
        )


def fib_cps_thunked(n, cont):
    if n <= 2:
        return cont(1)
    else:
        return lambda: fib_cps_thunked(
            n-1,
            lambda value1: fib_cps_thunked(
                n-2,
                lambda value2: cont(value1 + value2)
            )
        )


def main():
    try:
        print(fact_rec(1000))
    except RecursionError as e:
        print(f'RecursionError: {e}')
    # RecursionError: maximum recursion depth exceeded in comparison

    try:
        print(fact_cps(1000, end_cont))
    except RecursionError as e:
        print(f'RecursionError: {e}')
    # RecursionError: maximum recursion depth exceeded in comparison

    try:
        print(trampoline(fact_cps_thunked(1000, end_cont)))
    except RecursionError as e:
        print(f'RecursionError: {e}')
    # 40238726007709377354370243392300398571937486421071463254379...

    try:
        print(fib_cps(43, end_cont))
    except RecursionError as e:
        print(f'RecursionError: {e}')
    # RecursionError: maximum recursion depth exceeded in comparison

    try:
        print(trampoline(fib_cps_thunked(43, end_cont)))
    except RecursionError as e:
        print(f'RecursionError: {e}')
    # RecursionError: maximum recursion depth exceeded in comparison


if __name__ == '__main__':
    main()
