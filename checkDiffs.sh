echo data :
echo ----------- p0 p1
diff player0/data.py player1/data.py
echo p1 p2
diff player1/data.py player2/data.py
echo "_______"
echo transition :
echo p0 p1
diff player0/transition.py player1/transition.py
echo p1 p2
diff player1/transition.py player2/transition.py
echo p2 p0
diff player2/transition.py player0/transition.py
echo "_______"
echo main :
echo p0 p1
diff player0/main.py player1/main.py
echo p1 p2
diff player1/main.py player2/main.py
echo p2 p0
diff player2/main.py player0/main.py
