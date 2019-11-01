import math
import random


# Calculo do inverso modular de a e b 
def extendedEuclidean(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		gcd, x, y = extendedEuclidean(b % a, a)
		return (gcd, y - b//a * x, x)

################################################################################
################################################################################
################################################################################

# The Fermat primality test is a probabilistic test to determine whether a number is a probable prime.
def fermatPrimalityTest(n):
    if n > 1:
        for t in range(50):
            rand = random.randint(2, n)-1
            if pow(rand,n-1,n) != 1: # ?? eleva o número à n-1 ?
                return False
        return True
    else:
        return False

# Função para gerar primos: gera inteiros randômicos, e realiza o fermat test, caso seja falso, fermat de n+2
def geraPrimo(bits):
    n = random.randint(0, pow(2, bits))
    if n % 2 == 0:
        n = n+1

    while not fermatPrimalityTest(n):
        # print(n)
        n += 2

    return n
# Criador de chave pública
def chavePublica(bits):
	p = geraPrimo(bits)
	q = geraPrimo(bits)
	while p == q:
		q = geraPrimo(bits)

	e = random.randint(0, pow(2,16))
	while math.gcd(e, (p-1)*(q-1)) != 1:
		e = random.randint(0, pow(2,16))

	return (e, p, q)

# Criador de chave privada
def chavePrivada(e, p, q):
    d = extendedEuclidean(e, (p-1)*(q-1))[1] #Encontra o inverso modilar de p e q, 
    if d < 1:
        # print('burro') ?? kkkkk
        d = d + ((p-1)*(q-1))
    # print(d)

    return (int(d), p * q)
# utiliza a chave pública "e" e "n"
def criptografa(mensagem, e, n):
    cript = [] #Que função é esta?
    for c in mensagem:
        cript.append(pow(ord(c), e, n))

    return cript
# utiliza a chave privada "d" e "n"
def descriptografa(mensagem, d, n):
    decript = []
    for i in mensagem:
        #print(pow(i, d, n))
        decript.append(chr(pow(int(i), d, n)))

    return decript

def quebra_forcabruta(n):
	p = int(math.sqrt(n)) + 1

	if p % 2 == 0:
		p += 1

	while n % p != 0:
		p -= 2

	q = n // p

	return (p, q)

 # o que ser
def G(x,c):
	return pow(x,2) + c


# ???
def pollard_rho(n):
	x = random.randint(1, n)
	c = random.randint(1, n)
	y = x
	p = 1

	while p == 1:
		x = G(x, c) % n
		y = G(G(y, c), c) % n
		p = math.gcd(abs(x-y), n)

	return (p, n // p)


def main():
	bits = 64 # número de bits da chave ?!
	msg = open("msg.csv", "r") # não está encontrando este arquivo 
	encripted = open("cript.csv", "w")
	uncripted = open("uncript.csv", "w")
	e, p, q = chavePublica(bits) #gera a chave pública
	d, n = chavePrivada(e, p, q) #gera chave privada	
	a = criptografa(msg.read(), e, n) #encripta a msg
	# msg.truncate(0)
	# print(msg.read())
	for i in a: # laço para cada caractere da msg
		encripted.write(str(i))
		encripted.write(' ')

	encripted.close()
	encripted = open("cript.csv", "r")
	c = encripted.read().split()
	print(c==a)
	print(a)
	print('\n')
	print('\n')
	print(c)


	b = descriptografa(c, d, n)
	print(b)
	for j in b: # escreve a msg decriptada
		uncripted.write(str(j))
	msg.close()
	encripted.close()
	uncripted.close()

	print(d)
	print((p,q))
	print(pollard_rho(n))
	#print(quebra_forcabruta(n))


	# print(descriptografa(a, d, n))
	# print((p,q))
	# print(quebra_forcabruta(n, bits))


if __name__ == '__main__':
	main()
