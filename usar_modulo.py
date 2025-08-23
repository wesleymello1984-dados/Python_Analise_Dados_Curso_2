import meu_modulo as mm

usuarionascimento = int(input('\nInforme seu ano de nascimento: '))
usuarioatual = int(input('\nInforme o ano atual: '))

Idade = mm.Idade(usuarionascimento, usuarioatual)

print(f'Sua idade é: {Idade}.')
