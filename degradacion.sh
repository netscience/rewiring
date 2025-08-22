#!/bin/bash
source config.sh  # o . config.sh

for i in "${ARR[@]}"
do
    cp config.py $HOME$RESULTADOS_DIR/Degradación/$DEGRADACION/GrafosFinales/$i/ExperimentosCooperadores/R$REGLA/$RED/$ROUTING
    cp $FILE_DEGRADATION $HOME$RESULTADOS_DIR/Degradación/$DEGRADACION/GrafosFinales/$i/ExperimentosCooperadores/R$REGLA/$RED/$ROUTING
    cd $HOME$RESULTADOS_DIR/Degradación/$DEGRADACION/GrafosFinales/$i/ExperimentosCooperadores/R$REGLA/$RED/$ROUTING
    x=1
    while [ $x -le 10 ]
    do
        cp config.py $x
        cp $FILE_DEGRADATION $x
        cd $x
        echo "Comienza degradacion por $DEGRADACION $x del grafo del utlimo ciclo de simulacion..."
        c=$CICLOS
        while [ $c -ge 1 ]
        do
           archivo=graph_test_$c.adjlist
           if [ -f $archivo ]
           then
                $HOME$CONDA_DIR/python3 $FILE_DEGRADATION $archivo $HOME$RESULTADOS_DIR/Degradación/$DEGRADACION/GrafosFinales/$i/ExperimentosCooperadores/R$REGLA/$RED/$ROUTING/$x/
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
    cd $HOME$RESULTADOS_DIR
done