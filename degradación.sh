#!/bin/bash
declare -a arr=("D" "D2" "D4" "D8" "D16")
for i in "${arr[@]}"
do
    cp hubDegradation.py /home/jorge/Degradación/Ataques/GrafosFinales/$i/ExperimentosCooperadores/R1/anillo1500/CR
    cd /home/jorge/Degradación/Ataques/GrafosFinales/$i/ExperimentosCooperadores/R1/anillo1500/CR
    x=1
    while [ $x -le 10 ]
    do
        cp hubDegradation.py $x
        cd $x
        echo "Comienza degradacion por ataques $x del grafo del utlimo ciclo de simulacion..."
        c=50
        while [ $c -ge 1 ]
        do
           archivo=graph_test_$c.adjlist
           if [ -f $archivo ]
           then
                python3 hubDegradation.py $archivo /home/jorge/Degradación/Ataques/GrafosFinales/$i/ExperimentosCooperadores/R1/anillo1500/CR/$x/
                break
           else
                echo "$archivo NO existe"
           fi
           c=$(( $c - 1 ))
        done
        echo "Termina degradacion $x"
        cd ..
    x=$(( $x + 1 ))
    done
    cd ~
done