# Documentação TP0

**Aluno:** Igor Joaquim da Silva Costa

## Prova de funcionamento do código

Para comprovar o funcionamento do código, seguem as duas validações com um SAS contendo minha matrícula 2021032218 com o nonce 4. A primeira segue a validação usando IPv4 e segunda validação usando IPv6.

```bash
python3 client.py slardar.snes.2advanced.dev 51001 gtr 1 2021032218:4:0150c1d3f97f9b397f63179d7fc66650617336d63e7e1c7c8b7968770b0549f1
2021032218:4:0150c1d3f97f9b397f63179d7fc66650617336d63e7e1c7c8b7968770b0549f1+9fec06386c080f64fc9f83baf150ab6068ca5b671f57c72b199cc39b3396e450
 
python3 client.py 2001:12f0:601:a944:f21f:afff:fed5:967d 51001 gtr 1 2021032218:4:0150c1d3f97f9b397f63179d7fc66650617336d63e7e1c7c8b7968770b0549f1
2021032218:4:0150c1d3f97f9b397f63179d7fc66650617336d63e7e1c7c8b7968770b0549f1+9fec06386c080f64fc9f83baf150ab6068ca5b671f57c72b199cc39b3396e450
```

## Tutorial de execução do código

A interpretação do código se dá peço comando

```bash
python3 client.py $host $port $command
```

Além disso, existem exemplos de cada um dos tipos de comandos nos arquivos *.sh que acompanham a entrega.

## Problema com o Protocolo

Ao implementar o funcionamento de um cliente conectando a um servidor usando o protocolo proposto, é fácil notar que a noção de “autenticação” do protocolo se dá apenas por motivos educacionais. Em um cenário real, a autenticação provida é paralela a um sistema de login no qual o usuário apenas provê seu email, sem precisar da senha! Dessa forma - usando apenas o email como login - seu email público faz com que a sua autenticação também seja pública, ou seja, é fácil uma pessoa se passar por outro usuário.

Além disso, se alguém conseguir acessar o conteúdo dos pacotes que propagam na rede, o token também é facilmente obtido, visto que o mesmo é apenas uma sequência de ASCII.  

Complementando, um sistema de autenticação mais real precisaria de algum mecanismo de troca de senhas criptografadas para funcionar, como é caso da [autenticação SSH com chave pública](https://en.wikipedia.org/wiki/Public-key_cryptography#Hybrid_cryptosystems). Onde o servidor é responsável por dê criptografar a informação e validar a mesma