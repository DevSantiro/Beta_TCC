import os

def files_path06(*args):
    l = []
    for item in args:
        for p, _, files in os.walk(os.path.abspath(item)):
            for file in files:
                l.append((file))
    return l

array = files_path06('C:\\Repositorios_GIT\\Beta-TCC\\BetaTCC\\media\\arquivos_beta_glucosidase.fasta')

teste = 'beta_glucosidase.fasta.B99990001.pdb'

teste = teste.split('.')

extensao = teste[1:]

novo = ''

tamanho = len(extensao)
count = 1

for ext in extensao:
	if tamanho > count:
		novo += ext+"."
	else:
		novo += ext

	print(tamanho, count)

	count += 1

print(teste[1:])
print(novo)

print(array[0])