import os
import sys
import subprocess
import random
import time

def parse_score(name):
	fl = open(name, "r")
	fl.readline()
	s = fl.readline()
	a = float(s[13:])
	fl.close()
	return a

def make_best():
	f = open("reg_coefs2.txt", "r")
	a = f.readlines()
	f.close()
	f = open("best_coefs2.txt", "w")
	f.writelines(a)
	f.close()

def upload_best():
	f = open("best_coefs2.txt", "r")
        a = f.readlines()
        f.close()
        f = open("reg_coefs2.txt", "w")
        f.writelines(a)
        f.close()

def some_magic():
	a = []
	f = open("reg_coefs2.txt", "r")
	global change, fr, to
	#change = random.randint(0, 148)
	for i in range(148):
		b = (float(f.readline()))
		if (random.random() > 0.95):
			fr = b
			if random.random() > 0.2:
				to = random.random() * 5 * b
				a.append(to)
			elif random.random() > 0.995:
				to = 0
				a.append(to)
			else:
				to = random.random() * 5 * b * (-1)
				a.append(to)
		else:
			a.append(b)
	f.close()
	f = open("reg_coefs2.txt", "w")
	for i in range(148):
		f.write(str(a[i]))
		f.write("\n")
	f.close()
	f.close()



upload_best()
subprocess.call(["./BotExeTrain"], shell = True)
best_train = parse_score("res_train.txt")
subprocess.call(["./BotExeTest"], shell = True)
best_test = parse_score("res_test.txt")
best = best_test + best_train
i = 0
while (True):
	i = i + 1
	upload_best()
	some_magic()
	subprocess.call(["./BotExeTrain"], shell = True)
	a_train = parse_score("res_train.txt")
	subprocess.call(["./BotExeTest"], shell = True)
	a_test = parse_score("res_test.txt")
	a = a_train + a_test
	if a > best :
		sys.stdout.write(" [%d]Train best : %f   Test best : %f\n" % (i, best_train, best_test))
		sys.stdout.flush()
		best = a
		best_train = a_train
		best_test = a_test
		make_best()
	else:
		sys.stdout.write(" [%d]Train best : %f   Test best : %f\r" % (i, best_train, best_test))
		sys.stdout.flush()
