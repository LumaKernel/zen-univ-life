type Revolving = {
  // interest rate per year
  readonly rate_year: number;
  // pay per month
  readonly pay_month: number;
};
/**
 * f(x) := x - (pay_month - x * (rate_year / 12))
 * f^n(x)
 */
const fn = (x0: number, n: number, { rate_year, pay_month }: Revolving) => {
  const rate_month = rate_year / 12;
  const v = (1 + rate_month) ** n;
  return x0 * v - (v - 1) / rate_month * pay_month;
};

/**
 * Solve to find smallest n, s.t. f^n(x0) <= 0
 */
const pay_span = (x0: number, rev: Revolving) => {
  if (x0 <= 0) return 0;
  let upper = 1;
  while (fn(x0, upper, rev) > 0) {
    upper *= 2;
  }
  let lo = Math.floor(upper / 2);
  let hi = upper;
  while (hi - lo > 1) {
    const mid = Math.floor((lo + hi) / 2);
    if (fn(x0, mid, rev) <= 0) {
      hi = mid;
    } else {
      lo = mid;
    }
  }
  return hi;
};

console.log(pay_span(50, {
  rate_year: 0.15,
  pay_month: 0.7,
}));
