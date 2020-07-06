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
* Após realizada essa rotina usar o ID (do template com maior valor que nos foi apresentado) e realizar o Download de forma automática através do PDB, comando: https://files.rcsb.org/download/"+id_maior+".pdb"


# Alinhamento

* Preparar o processo automático de Alinhamento (Ainda preciso estudar este caso).

# Modeller

* Executar o Modeller após o Alinhamento (Estudar o caso)

# Identificar o Melhor modelo

* Identificar o melhor modelo gerado (através do score?)


############# Fim do Fluxo do Pipeline ############# 

4º Elaborar uma forma de apresentação

4.1 - Baixar ou apresentar o resultado


############# Fim do Fluxo de Pipeline e Apresentação ############# 