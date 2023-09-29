COUNTER=1
# while [ true ]
# do
echo $COUNTER
pypy3 learn.py & pypy3 learn.py & pypy3 learn.py & pypy3 learn.py & pypy3 learn.py & pypy3 learn.py
wait
python mutate.py
((COUNTER++))
# done