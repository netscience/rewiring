#!/bin/bash
#pasar como argumento un 1 si se trabaja con malla o un 3 si se trabaja con anillo
#activa el ambiente de conda
# Cargar las variables desde config.sh
source config.sh  # o . config.sh
declare -a arr=("D" "D2" "D4" "D8" "D16")
for i in "${arr[@]}"
do
    cd Formación/$i/ExperimentosCooperadores/R1/malla50x50/CR
    # You can access the array items using echo "${arr[0]}", "${arr[1]}" also
    x=1
    while [ $x -le 10 ]
    do
        echo "Inicia la simulacion $x ..."
        mkdir $x
        #python se ejecuta desde el environment
        #python3 main.py > $x/salida_$x.txt 
        $HOME$CONDA_DIR/python3 main.py > $x/salida_$x.txt
        echo "Termina la simulacion $x"
        cp extractData.py $x
        if [ "$1" = "1" ]
        then 
          echo "Trabajas con una malla"
        else
          echo "Trabajas con un anillo"
        fi
        #graph.adjlist es el grafo original (malla o anillo) creado por main.py
        cp graph.adjlist $x/graph.adjlist
        cd $x
        echo "Comienza extraccion de datos $x ..."
        $HOME$CONDA_DIR/python3 extractData.py salida_$x.txt  test
        echo "Termina extraccion de datos $x"
        cd ..
    x=$(( $x + 1 ))
    done
    cd $HOME$RESULTADOS_DIR 
done