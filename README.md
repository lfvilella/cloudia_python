# cloudia_python
Teste para Desenvolvedores Python

# Fizz Buzz Bot
O projeto consiste em construir um bot para o Facebook Messenger ou Telegram que responda automaticamente mensagens direcionadas a ele com a lógica "Fizz Buzz".

## Sobre as tecnologias que devem ser usadas:
- Flask como framework web da aplicação;
- Requisições de API devem ser tratadas utilizando arquitetura REST;
- Banco de dados relacional MySQL;
- Pytest como framework de teste unitário.
> O projeto deve seguir boas práticas de programação e design de código.

## Requisitos funcionais e de qualidade:
- O bot deve receber como entrada qualquer texto com até 280 caracteres e responder caso seja um número inteiro.
- A resposta deverá ser "Fizz" caso o número seja múltiplo de 3, "Buzz" caso o número seja múltiplo de 5 ou "FizzBuzz" caso seja múltiplo de 3 e de 5.
- O bot deverá responder com a mesma entrada caso não se enquadre em nenhum caso descrito de "FizzBuzz".
- Ou responder com uma mensagem padrão caso a entrada não seja um número inteiro válido.
- O bot deverá armazenar as informações dos usuários que interagirem com o bot;
- Assim como armazenar também as mensagens trocadas com estes usuários.
- Desenvolver testes unitários para a aplicação;

## Diferenciais que somam pontos extras ao projeto:
- Utilização de containers Docker;
- Deploy da aplicação na AWS.

## Contato e dúvidas
Você pode (e deve) a qualquer momento entrar em contato pelo email lucasalveslm@gmail.com para tirar dúvidas sobre requisitos.

## Critérios de avaliação:
Iremos avaliar a qualidade do código sob todos os aspectos. Listamos aqui alguns pontos para se ter atenção:
- Escreva código limpo e claro.
- Respeite os dialetos das linguagens.
- Utilizar padrões bem estabelecidos para resolver os problemas propostos.
- Priorize suas atividades levando em consideração:
    - Entrega dos requisitos mínimos > Qualidade do código > Testes unitários > Deploy na AWS.
- Sempre que julgar importante, utilize bibliotecas de código aberto que possam te ajudar no desenvolvimento.
Collapse


# Running Locally

1) Clone the project :)
2) Set your credentials on .env
3) make build
4) make up

## Bot running

Bot Facebbok: [click here](https://m.me/427453708173711)

![facebook_bot](https://user-images.githubusercontent.com/45940140/90322215-e3653200-df27-11ea-883c-6db8a666294c.gif)

Bot Telegram: [click here](https://web.telegram.org/#/im?p=@cloudia_fizzbuzz_bot)

![telegram_bot](https://user-images.githubusercontent.com/45940140/90322240-6d14ff80-df28-11ea-8fdf-6dfb877c91a5.gif)
