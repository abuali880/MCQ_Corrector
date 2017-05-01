# n = raw_input()
# b = 1
# l = []
# for x in xrange(0,10000):
# 	b = 3*x
# 	l.append(b)
# 	pass
# n = str(n)
# x = 999
# while x >= 0:
# 	v = n.find(str(l[x]))
# 	if v != -1:
# 		v = l[x]
# 		break
# 		pass
# 	x = x - 1
# 	pass
# print v

f1 = open("output.csv")
f2 = open("result.csv")
c = 0
count =0
acc = 0
while 1 == 1:
    n1 = f1.readline()
    n2 = f2.readline()
    if n1 =='' and n2 == '':
        break
    n1 = n1.split(",")
    n2 = n2.split(",")
    #n2[1] = n2[1].replace("\n", "")
    if n1[1] != n2[1]:
        print n1[0],n1[1]
        print "your answer: " + str(n2[1])
        count += 1
        acc += abs(int(n1[1])-int(n2[1]))

print "Fault in questions: " + str(acc)
print "No of non correct papers: "+ str(count)
