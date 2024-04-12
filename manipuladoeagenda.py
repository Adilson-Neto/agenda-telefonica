import json

contatos_suportados = ("telefone", "email", "endereco")


def contato_para_texto(nome_contato:str, **formas_contato):
    formato_texto = f"{nome_contato}"
    for meio_contato, contato in formas_contato.items():
        formato_texto = f"{formato_texto}\n{meio_contato.upper()}"
        contador_formas =1
        for valor in contato:
            formato_texto = f"{formato_texto}\n\t{contador_formas} - {valor.upper()}"
            contador_formas = contador_formas + 1

    return formato_texto


def agenda_para_texto(**agenda_completa):
    formato_texto = ""
    for nome_contato, formas_contato in agenda_completa.items():
        formato_texto = f"{formato_texto} {contato_para_texto(nome_contato, **formas_contato)}\n"
        formato_texto = f"{formato_texto}-------------------------\n"
    return formato_texto


def altera_nome_contato(agenda_original:dict, nome_original:str, nome_atualizado:str):
    if nome_original in agenda_original.keys():
        copia_contatos = agenda_original[nome_original].copy()
        agenda_original.pop(nome_original)
        agenda_original[nome_atualizado] = copia_contatos
        return True
    return False


def altera_forma_contato(lista_contatos:list, valor_antigo:str, novo_valor:str):
    if valor_antigo in lista_contatos:
            posicao_valor_antigo = lista_contatos.index(valor_antigo)
            lista_contatos.pop(posicao_valor_antigo)
            lista_contatos.insert(posicao_valor_antigo, novo_valor)
            return True
    return False


def exclui_contato(agenda:dict, nome_contato: str):
    if nome_contato in agenda.keys():
        agenda.pop(nome_contato)
        return True
    return False


def inclui_contato(agenda:dict, nome_contato:str, **formas_contato):
    agenda [nome_contato] = formas_contato


def inclui_forma_contato(formas_contato:dict, forma_incluida:str, valor_incluido:str):
    if forma_incluida in formas_contato.keys():
        formas_contato[forma_incluida].append(valor_incluido)
        return True
    elif forma_incluida in contatos_suportados:
        formas_contato[forma_incluida] = [valor_incluido]
        return True
    return False


def usuario_inclui_contato(agenda:dict):
    nome = input("informe o nome do novo contato que será inserido na agenda: ")
    dicionario_formas = {}
    for forma in contatos_suportados:
        resposta = input(f"deseja inserir um {forma} para {nome.upper()}? \n SIM OU NÃO -> ")
        lista_contatos = []
        while "S" in resposta.upper():
            lista_contatos.append(input(f"informe um {forma}:"))
            resposta= input(f"deseja inserir outro {forma} para {nome.upper()}?\n SIM OU NÃO ->")
        if len (lista_contatos)> 0:
            dicionario_formas[forma] = lista_contatos.copy()
            lista_contatos.clear()
    if len(dicionario_formas.keys()) > 0:
        inclui_contato(agenda, nome, **dicionario_formas)
        print("inclusão bem sucedida! ")
    else:
        print("É necessário incluir pelo menos uma forma de contato! \n A agenda não foi alterada.")


def usuario_inclui_forma_contato(agenda:dict):
    nome = input("Informe o nome do contato para qual deseja incluir formas de contato")
    if nome in agenda.keys():
        print(f"As formas de contato suportadas pelo sistema são: {contatos_suportados}")
        forma_incluida = input("Qual forma de contato deseja incluir? ")
        if forma_incluida in contatos_suportados:
            valor_incluido = input(f"informe o {forma_incluida} que deseja incluir: ")
            if inclui_forma_contato(agenda[nome], forma_incluida, valor_incluido):
                print("Operação bem sucedida! A nova forma de contato foi Incluida!")
            else:
                print("Ocorreu um erro durante a inserção. A agenda não foi alterada.")
        else:
             print("A forma de contato indicada não é suportada pelo sistema. A agenda não foi alterada.")
    else:
        print("O contato informado não existe na agenda. Não foram feitas alterações." )


def usuario_exclui_contato(agenda:dict):
    nome = input("Informe o nome do contato que deseja excluir: ")
    if exclui_contato(agenda, nome):
        print("Usuário excluido com sucesso!")
    else:
        print("Nome do usuário não localizado na agenda. Não foram feitas alterações.")


def usuario_altera_nome_contato(agenda:dict):
    nome_original = input("Informe o nome do contato que deseja alterar: ")
    nome_atualizado = input("informe o nome do novo contato: ")
    if altera_nome_contato(agenda, nome_original, nome_atualizado):
        print(f"O contato foi atualizado e agora se chama {nome_atualizado}")
    else:
        print(f"O contato original não foi localizado. A agenda não foi alterada.")


def usuario_altera_forma_contato(agenda:dict):
    nome = input("Informe o nome do contato que deseja alterar: ")
    if nome in agenda.keys():
        print(f"As formas de contato suportadas pelo sistema são: {contatos_suportados}")
        forma_incluida = input("Qual forma de contato deseja incluir? ")
        if forma_incluida in contatos_suportados:
            print(contato_para_texto(nome, **agenda[nome]))
            valor_antigo = input(f"Informe o {forma_incluida} que deseja alterar ")
            nova_valor = input(f"Informe o novo {forma_incluida} ")
            if altera_forma_contato(agenda[nome][forma_incluida], valor_antigo, nova_valor):
                print("Contato alterado com sucesso!")
            else:
                print("Ocorreu um erro durante a alteração do contato. A agenda nao foi alterada! ")
        else:
            print(f"{forma_incluida} não é uma forma de contato suportada pelo sistema. A agenda não foi alterada.")
    else:
         print(f"O contato {nome} não está na agenda. A agenda não foi alterada.")


def usuario_contato_para_texto(agenda:dict):
    nome = input("informe o nome do contato que deseja ixibir: ")
    if nome in agenda.keys():
        print(contato_para_texto(nome, **agenda[nome]))
    else:
        print("O contato informado não está na agenda. ")


def agenda_para_txt(nome_arquivo:str, agenda):
    if "txt" not in nome_arquivo:
        nome_arquivo = f"{nome_arquivo}.txt"
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(agenda_para_texto(**agenda))
        print("Agenda exportada com sucesso!")


def json_para_agenda(nome_arquivo:str):
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()
    print("Agenda carregada com sucesso!")
    return json.loads(conteudo)


def agenda_para_json(nome_arquivo:str, agenda):
    if ".json" not in nome_arquivo:
        nome_arquivo = f"{nome_arquivo}.json"
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(json.dumps(agenda, indent=4, ensure_ascii=False))
            print("Agenda exportada com sucesso!")


def exibe_menu():
    print("\n\n")
    print("1 - Incluir contato na agenda")
    print("2 - Incluir uma forma de contato")
    print("3 - Alterar o nome de um contato")
    print("4 - Alterar uma forma de contato")
    print("5 - Exibir um contato")
    print("6 - Exibir toda a agenda")
    print("7 - Excluir um contato")
    print("8 - Exportar agenda para TXT")
    print("9 - Exportar agenda para Json")
    print("10 - Importar agenda para Json")
    print("11 - Sair")
    print("\n")


def manipulador_agenda():
    agenda = {}
    op = 1
    while op != 11:
        exibe_menu()
        op = int(input("informe a opção desejada: "))
        if op == 1:
            usuario_inclui_contato(agenda)
        elif op == 2:
            usuario_inclui_forma_contato(agenda)
        elif op == 3:
            usuario_altera_nome_contato(agenda)
        elif op == 4:
            usuario_altera_forma_contato
        elif op == 5:
            usuario_contato_para_texto(agenda)
        elif op == 6:
           print(agenda_para_texto(**agenda))
        elif op == 7:
            usuario_exclui_contato(agenda)
        elif op == 8:
            nome_arquivo = input("Informe o nome ou caminho do arquivo:")
            agenda_para_txt(nome_arquivo, agenda)
        elif op == 9:
            nome_arquivo = input("Informe o nome ou caminho do arquivo:")
            agenda_para_json(nome_arquivo, agenda)
        elif op == 10:
            nome_arquivo = input("Informe o nome ou caminho do arquivo: ")
            agenda = json_para_agenda(nome_arquivo)
        elif op == 11:
            print(f"encerrando sistema...")
            break
        else:
            print("Opção invalida! informe uma opção existente.")

manipulador_agenda()