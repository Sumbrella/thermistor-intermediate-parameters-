from numpy import log, exp
from scipy.optimize import curve_fit
from gooey import Gooey, GooeyParser


def parse_args(args):
    result = dict()
    for key, val in vars(args).items():
        if val is not None:
            try:
                result[key] = int(val)
            except ValueError:
                result[key] = float(val)
        else:
            result[key] = None
    return result


def rt_t_function(t, b, ln_r25):
    return b * (1 / (273 + t) - 1 / 298) + ln_r25


def check_args(args):
    groups = args['n']
    count = 0
    for i in range(groups):
        rt_i = args["r{}".format(i)]
        t_i = args["t{}".format(i)]
        if rt_i and t_i:
            count += 1
    if count < groups:
        raise Exception("输入数据不足! 需要{}组，实际输入{}组"
                        .format(groups, count))


def process(args):
    args = parse_args(args)
    check_args(args)
    n = args['n']
    rt = [args['r{}'.format(i)] for i in range(n)]
    ln_rt = [log(args['r{}'.format(i)]) for i in range(n)]
    t = [args['t{}'.format(i)] for i in range(n)]
    popt, _ = curve_fit(rt_t_function, t, ln_rt)
    r25 = exp(rt_t_function(25, *popt))
    r45 = exp(rt_t_function(45, *popt))
    r65 = exp(rt_t_function(65, *popt))
    print("Bn ={:.5f}\nr25={:.5f}\nr45={:.5f}\nr65={:.5f}"
          .format(popt[0], r25, r45, r65))


@Gooey(
    program_name="热敏电阻Rt-t参数确定",
    language="english"
)
def main():
    parser = GooeyParser()
    parser.add_argument(
        "n",
        metavar="实验组数",
        help="选择数据组数",
        default='8',
        choices=[str(i) for i in range(4, 13)]
    )

    for i in range(12):
        group = parser.add_argument_group()
        group.add_argument(
            "-t{}".format(i),
            metavar="t-{}".format(i + 1)
        )
        group.add_argument(
            "-r{}".format(i),
            metavar="Rt-{}".format(i + 1)
        )

    args = parser.parse_args()

    process(args)


if __name__ == '__main__':
    main()
