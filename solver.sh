COUNTER=1
while [ true ]
do
    echo ""
    echo "ROUND $COUNTER"
    echo ""
    rm scores.json
    pypy3 learn.py & pypy3 learn.py & pypy3 learn.py & pypy3 learn.py & pypy3 learn.py & pypy3 learn.py
    wait
    rm genomes_$COUNTER -rf
    mkdir genomes_$COUNTER
    cp genomes/* genomes_$COUNTER
    cp scores.json genomes_$COUNTER
    python mutate.py
    ((COUNTER++))
done