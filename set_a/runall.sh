al26_nbody_loc="../al26_nbody/al26_nbody_agb_cyl.py"
export al26_nbody_loc

execute () {
  echo Running name $1 radius $2 mass $3 velocity $4
  mkdir $1
  cd $1
  for n in {1..50}
  do
    mkdir $1-$n
    cd $1-$n
    ntry=0
    until [ "$ntry" -ge 5 ]
    do
      python3 $al26_nbody_loc -n 100 -rc $2 -rd 400 -f $1-$n -m fractal -i -di 1.0 -mi $3 -rbi 0.1 -ri 0.0 -vi $4 --no_massive_star_requirement --star_min_mass 0.1 --star_max_mass 50 && break
    done
    cd ..
  done
  cd ..
}

export -f execute

rc_list="0.3 0.1 1.0"
mi_list="7 3"
vi_list="1.0 3.0 10.0 30.0 100.0"

for rc in $rc_list
do
  mkdir pt-$rc
  cd pt-$rc
  parallel -j 5 --colsep ' ' execute pt-rc-$rc-inm-{1}-inv-{2} $rc {1} {2} ::: $mi_list ::: $vi_list
  cd ..
done