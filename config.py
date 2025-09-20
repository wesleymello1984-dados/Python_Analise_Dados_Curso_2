#  ___       ___    _____    _____   _____        _____  __      __
# (  (       )  )  / ___/   / ____\ (_   _)      / ___/  ) \    / (
#  \  \  _  /  /  ( (__    ( (___     | |       ( (__     \ \  / / 
#   \  \/ \/  /    ) __)    \___ \    | |        ) __)     \ \/ /  
#    )   _   (    ( (           ) )   | |   __  ( (         \  /   
#    \  ( )  /     \ \___   ___/ /  __| |___) )  \ \___      )(    
#     \_/ \_/       \____\ /____/   \________/    \____\    /__\   
                                                                 
#    __    __      _____   _____       _____         ____          
#    \ \  / /     / ___/  (_   _)     (_   _)       / __ \         
#    () \/ ()    ( (__      | |         | |        / /  \ \        
#    / _  _ \     ) __)     | |         | |       ( ()  () )       
#   / / \/ \ \   ( (        | |   __    | |   __  ( ()  () )       
#  /_/      \_\   \ \___  __| |___) ) __| |___) )  \ \__/ /        
# (/          \)   \____\ \________/  \________/    \____/         

# Autor: Wesley Mello
# Data: 20/09/2025
# versão: 1.0.0

# Configurações comuns do sistema 

folder = r'C:/Users/sabado/Desktop/Python AD - Wesley/AIS/'
bd_path = "BancoDeDadosIAS.bd"
flask_debug = True
flask_host = '127.0.0.1'
flask_port = 5000

# Rotas comuns do sistema

rotas = [
    '/',                        # rota 00
    '/upload',                  # rota 01
    '/consultar',               # rota 02
    '/graficos',                # rota 03
    '/editar_inadimplencia',    # rota 04
    '/correlacao'               # rota 05
]

