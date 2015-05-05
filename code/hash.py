#!/usr/bin/python
def hash(selfuin, ptwebqq):
	selfuin += ""
	N=[0,0,0,0]
	for T in range(len(ptwebqq)):
		N[T%4]=N[T%4]^int(ptwebqq[T])

	
	U=["EC","OK"]
	V=[0, 0, 0, 0]
	V[0]=int(selfuin) >> 24 & 255 ^ ord(U[0][0])
	V[1]=int(selfuin) >> 16 & 255 ^ ord(U[0][1])
	V[2]=int(selfuin) >>  8 & 255 ^ ord(U[1][0])
	V[3]=int(selfuin)       & 255 ^ ord(U[1][1])

	U=[0,0,0,0,0,0,0,0]
	U[0]=N[0];
	U[1]=V[0];
	U[2]=N[1];
	U[3]=V[1];
	U[4]=N[2];
	U[5]=V[2];
	U[6]=N[3];
	U[7]=V[3];

	N=["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"];
	V="";
	for T in range(len(U)):
		V+= N[ U[T]>>4 & 15]
		V+= N[ U[T]    & 15]

	return V

#-----Test------------
testHashValue = hash ("752584911", "123456789")
print testHashValue
