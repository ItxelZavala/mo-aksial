import structlog
from scipy import optimize
from sympy import Symbol, lambdify

logger = structlog.get_logger()


def aksial(expression, x_0, epsilon):
    k, num_j = 0, 2
    x1, x2 = Symbol('x1'), Symbol('x2')
    d = [
        (1, 0),
        (0, 1)
    ]

    # array berisi nilai x dari 0 sampai k
    x = [x_0]

    # expression dalam bentuk function python
    f = lambdify((x1, x2), expression)

    # array berisi hasil f(xk) dimulai dari index 0
    f_x = [f(*x_0)]

    logger.msg('Initial values.', x_0=x_0, epsilon=epsilon, f=expression, f_x=f_x, d=d)

    while True:
        y = [None] * (num_j + 1)
        y[0] = x[k]

        logger.msg('Working on iteration.', k=k, y=y, x=x)

        for j in range(num_j):
            l = Symbol('l')
            param = (y[j][0] + d[j][0] * l, y[j][1] + d[j][1] * l)
            logger.msg('Working on loop.', j=j, param=param)

            f_l = f(*param)
            logger.msg('Compute f(l).', f_l=f_l)

            def the_func(a):
                return f_l.evalf(subs={l: a})

            res = optimize.minimize(the_func, 0)
            if res.success is not True:
                logger.msg('Failed to find minimum solution.', )
                return

            y[j + 1] = (y[j][0] + res.x[0] * d[j][0], y[j][1] + res.x[0] * d[j][1])
            logger.msg('Loop complete!', k=k, j=j, y=y)

        f_xk = f(*y[num_j])
        logger.msg('Compute f_xk', y=y, f_xk=f_xk)

        # check stop condition
        error = abs(f_xk - f_x[k])
        logger.msg('Compute error', error=error)
        if error < epsilon:
            print
            logger.msg('Error is less than epsilon!')
            logger.msg('Got solution!', f_min=f_xk, x_min=y[num_j], k=k + 1)
            return

        k += 1
        f_x.append(f_xk)
        x.append(y[num_j])
        logger.msg('Iteration complete!', x=x, f_x=f_x)
        print


if __name__ == '__main__':
    print("Program ini menyelesaikan minimalkan x pada\n"
          "(x1 + x2^3)^2 + 2*(x1 - x2 - 4)^4 + 3*(x1 + x2)\n"
          "Dengan x0=(10;0) dan toleransi epsilon=0.001")
    print

    x1, x2 = Symbol('x1'), Symbol('x2')
    expression = (x1 + x2 ** 3) ** 2 + 2 * (x1 - x2 - 4) ** 4 + 3 * (x1 + x2)
    aksial(expression, (10, 0), 0.001)
