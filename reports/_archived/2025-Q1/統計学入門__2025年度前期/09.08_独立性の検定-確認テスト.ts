type Vec = readonly number[];
type Mat = readonly Vec[];

function sum(vec: Vec) {
  return vec.reduce((x, y) => x + y, 0);
}
function rowSum(mat: Mat): Vec {
  return mat.map((row) => sum(row));
}
function colSum(mat: Mat): Vec {
  const temp = mat[0].map(() => 0);
  for (const row of mat) {
    for (const [i, el] of row.entries()) {
      temp[i] += el;
    }
  }
  return temp;
}
function matSum(mat: Mat): number {
  return mat.reduce((acc, row) => acc + sum(row), 0);
}
function mapMat(
  mat: Mat,
  mapFn: (el: number, ri: number, ci: number) => number,
): Mat {
  return mat.map((row, ri) => row.map((el, ci) => mapFn(el, ri, ci)));
}
function indep_test_value(obs: Mat) {
  const row_sums: Vec = rowSum(obs);
  const col_sums: Vec = colSum(obs);
  const all_sum = matSum(obs);
  const exp = mapMat(obs, (_el, ri, ci) => {
    const p_row = row_sums[ri] / all_sum;
    const p_col = col_sums[ci] / all_sum;
    const p = p_row * p_col;
    return p * all_sum;
  });

  const chi_mat = mapMat(obs, (o, ri, ci) => {
    const exp_val = exp[ri][ci];
    return (o - exp_val) ** 2 / exp_val;
  });

  return matSum(chi_mat);
}

const v = indep_test_value([[36, 64], [44, 56]]);
console.log(v);
