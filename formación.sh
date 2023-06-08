#!/bin/bash
#pasar como argumento un 1 si se trabaja con malla o un 3 si se trabaja con anillo
declare -a arr=("D" "D2" "D4" "D8" "D16")
for i in "${arr[@]}"
do
    cd Formación/$i/ExperimentosCooperadores/R1/anillo1500/CR
    # You can access the array items using echo "${arr[0]}", "${arr[1]}" also
    x=1
    while [ $x -le 10 ]
    do
        echo "Inicia la simulacion $x ..."
        mkdir $x
        python3 main.py > $x/salida_$x.txt 
        echo "Termina la simulacion $x"
        cp extractData.py $x
        if [ "$1" = "1" ]
        then 
          echo "Trabajas con una malla"
          #malla.adjlist es el grafo original
          cp malla.adjlist $x/graph.adjlist
        else
          #anillo.adjlist es el grafo original
          echo "Trabajas con un anillo"
          cp anillo.adjlist $x/graph.adjlist
        fi
        cd $x
        echo "Comienza extraccion de datos $x ..."
        python3 extractData.py salida_$x.txt  test
        echo "Termina extraccion de datos $x"
        cd ..
    x=$(( $x + 1 ))
    done
    cd ~  
done