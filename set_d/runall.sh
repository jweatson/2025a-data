al26_nbody_loc="../al26_nbody/al26_nbody_agb_cyl.py"
export al26_nbody_loc

execute () {
  SIMS=$(expr 6000 / $6)
  echo Running name $1 radius $2 mass $3 velocity $4 bubble radius $5 population size $6 SIMS $SIMS
  mkdir $1
  cd $1
  for n in $(seq 1 $SIMS)
  do
    mkdir $1-$n
    cd $1-$n
    ntry=0
    until [ "$ntry" -ge 5 ]
    do
      python3 $al26_nbody_loc -n $6 -rc $2 -rd 400 -f $1-$n -m fractal -i -di 2.0 -mi $3 -rbi $5 -ri 0.0 -vi $4 --no_massive_star_requirement --star_min_mass 0.1 --star_max_mass 50 && break
    done
    cd ..
  done
  cd ..
}

export -f execute

rc_list="0.3"
mi_list="7"
rb_list="0.1"
vi_list="1.0 3.0 10.0 30.0"
ns_list="1000 500 300 100"

for rc in $rc_list; do
  mkdir -p pt-$rc
  cd pt-$rc
  parallel -j 5 --colsep ' ' execute pt-rc-$rc-inm-{1}-inv-{2}-rb-{3}-ns-{4} $rc {1} {2} {3} {4} ::: $mi_list ::: $vi_list ::: $rb_list ::: $ns_list
  cd ..
done


# python3 al26_nbody.py -n 100 -rc 0.1 -m fractal -f test -i -mi 3 -ri 0.1 -vi 0.0 -v
