# Beta_TCC

################## Fluxo de Desenvolvimento ##################

1º Criar um ambiente de cadastro de 1º Proteina que vou utilizar como Referência

1.1 - Criar um banco de dados para cadastrar essa proteina.

1.2 - Listar as proteinas cadastradas.

1.3 - Criar uma tela para exibir as informações dessa proteina ao clicar na mesma.

2º Tela de apresentação da Proteina será responsável por gerar o modelo através do pipeline

2.1 - Trazer as informações básicas dessa Proteina a tela.

2.2 - Criar um botão de ação (javaScript || Jquery), responsável por disparar a rotina de execução.

3º Rotina de execução (Desenvolvimento das Chamadas do Pipeline)

3.1 - Ao clicar no botão de ação preciso vincular o ID da proteina selecionada e puxar as informações do seu respectivo registro no meu banco de dados.

3.2 - Ao conseguir as informações preciso dividir as etapas de execução do pipeline (preparar todo o fluxo de evento) 

Fluxo de Eventos para a modelagem:

# Blast

* Realizar o Blast através de 2 arquivos (Minha Proteina Base e um arquivo com várias proteinas da mesma familia afim de identificar o template com maior identidade).


# Alinhamento

* Preparar o processo automático de Alinhamento.
* O precesso é dado a partir da leitura de 2 arquivos:
  1º Arquivo da Proteina em questão (no caso estou utilizando a Beta-glucosidase), utilizo o clustalw para Alinhar.
  2º Arquivo template referente a esta proteina, o arquivo template é no formato .pdb (Após pesquisas, estou utilizando o arquivo 4hpg.pdb para esta proteina em questão)
 

# Modeller

* Executar o Modeller após o Alinhamento.
* Instalei o Modeller dentro do meu Projeto Django e configurei todo o ambiente para poder ser executado através do meu código fonte, aqui eu crio um script em Python (dinâmico) e uso o "mod9.24 run.py" para a execução da rotina, atualmente gero 3 modelos, mas é possivel alterar via código fonte. (Cada modelo leva cerca de 30s para finalizar).

# Identificar o Melhor modelo

* Identificar o melhor modelo gerado (através do score?)


############# Fim do Fluxo do Pipeline ############# 

4º Elaborar uma forma de apresentação

4.1 - Baixar ou apresentar o resultado


############# Fim do Fluxo de Pipeline e Apresentação ############# 
