al26_nbody_loc="../al26_nbody/al26_nbody_agb_cyl.py"
export al26_nbody_loc

xs=$(python3 ../linspace.py 0 8 64)
ys=$(python3 ../linspace.py 0 1 8)

generate_cmd() {
  v=$1
  x=$2
  y=$3
  c=$4
  dirname="run-$c"
  echo $dirname vel $v x = $x y = $y $c
  mkdir $dirname
  cd $dirname

  ntry=0
  until [ "$ntry" -ge 10 ]
  do
    python3 $al26_nbody_loc -n 100 -rc 0.3 -rd 400 -f $dirname -m fractal -i -mi 7.0 -di $x -rbi 0.1 -vi $v -ri $y -ti 0.0 --no_massive_star_requirement --star_min_mass 0.1 --star_max_mass 50 --interloper_trajectory && break
    ntry=$((ntry+1))
    sleep 10
  done
  cd ..
}

export -f generate_cmd

for v in 30.0 10.0 3.0 1.0; do
  mkdir vel-$v
  cd vel-$v
  parallel -j 5 --colsep ' ' generate_cmd $v {1} {2} {#} ::: $xs ::: $ys
  cd ..
done



