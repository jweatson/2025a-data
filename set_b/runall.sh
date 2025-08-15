al26_nbody_loc="../al26_nbody/al26_nbody_agb_cyl.py"

vs=$(python3 ../logspace.py -1 2 32)
ts=$(python3 ../logspace.py -2 1 32)

mkdir pt-0.3
cd pt-0.3
c=0
export al26_nbody_loc

generate_cmd() {
  v=$1
  t=$2
  c=$3
  dirname="run-$c"
  mkdir -p "$dirname"
  cd "$dirname"
  echo $v $t $c $dirname
  ntry=0
  until [ "$ntry" -ge 5 ]; do
    python3 "$al26_nbody_loc" -n 100 -rc 0.3 -rd 400 -f "$dirname" -m fractal -i -mi 7.0 -di 1.0 -rbi 0.1 -ri 0.0 -vi "$v" -ti "$t" --no_massive_star_requirement --star_min_mass 0.1 --star_max_mass 50 --interloper_trajectory && break
    ntry=$((ntry+1))
    sleep 10
  done
  cd ..
}

export -f generate_cmd

parallel -j 4 --colsep ' ' generate_cmd {1} {2} {#} ::: $vs ::: $ts
