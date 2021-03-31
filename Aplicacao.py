#encoding: utf-8

from tkinter import Tk, StringVar, Frame,Entry,Label,Button,Menu,BooleanVar,Checkbutton,PhotoImage,END,RIGHT,LEFT,TOP,BOTTOM,CENTER,VERTICAL,Y,HORIZONTAL,X
from tkinter import messagebox
from tkinter import ttk
from Banco import Banco
import pandas as pd
from variaveis import *
from Classes import AutocompleteCombobox 

#Criar Janela
jan = Tk()

#CONFIGURACOES ----
#Titulo
jan.title(titulos)
#Tamanho da Janela
jan.geometry(str(largura)+"x"+str(altura))
#Cor de Fundo
jan.configure(background = cor_meta)
#Nao redimensionar
jan.resizable(width = False, height = False)
#Transparencia
jan.attributes("-alpha",0.95)
#Icone
jan.iconbitmap(default="Icons/icon.ico")
#Logo
logo = PhotoImage(file="icons/logo_.png")


#FUNÇÕES
def Mensagem_Aviso(txt):
    ''' Aviso para caso falte alguma informação válida'''
    messagebox.showerror(title="Impossível Cadastrar Atendimento", message= txt)

def Inserir():
    global lista_locais, lista_atendimentos, lista_certificados, lista_solicitantes, qtd, listagem

    txt = ""
    
    #LOCAL
    local = localEntry.get().upper()
    if local == "":
        txt += "Local Inválido!\n"
    elif local not in lista_locais :
        add_local = messagebox.askyesno(title="Aviso!", message="Esse Local Não Está Cadastrado. Deseja Cadastrá-lo?" )
        if add_local: 
            lista_locais.append(local)
            localEntry.set_completion_list(lista_locais)
        else:
            localEntry.delete(0,END)
            return 

    #SOLICITANTE
    solicitante = solEntry.get().upper()
    if solicitante not in lista_solicitantes:
        txt = txt + "Solicitante Inválido!\n"

    #ATENDIMENTO
    atendimento = atendEntry.get().upper()
    if atendimento == "":
        txt += "Atendimento Inválido!\n"
    elif atendimento not in lista_atendimentos:
        add_atend = messagebox.askyesno(title="Aviso!", message="Esse Atendimento Não Está Cadastrado. Deseja Cadastrá-lo?" )
        if add_atend: 
            lista_atendimentos.append(local)
            atendEntry.set_completion_list(lista_atendimentos)
        else:
            atendEntry.delete(0,END)
    
    #TIPO DE CERTIFICADO
    certificado = certEntry.get().upper()
    if certificado not in lista_certificados:
        txt = txt + "Tipo de Certificado Inválido!\n"

    #DISPOSITIVO DA META
    meta = "SIM"
    if not chkValueMeta.get():
        meta = "NAO"

    #PROBLEMA RESOLVIDO
    resolv = "SIM"
    if not chkValueResol.get():
        resolv = "NAO"

    #CASO TUDO ESTEJA CORRETO
    if txt == "":
        
        #CADASTRA NO BANCO DE DADOS
        banco = Banco()
        ultimo = banco.current
        x = banco.dados["Id"]
        print(ultimo, x[ultimo-1])
        id_ = str(int(x[ultimo-1]) + 1)
        nova_linha = [id_,local, solicitante, atendimento, certificado, meta, resolv, data]        
        banco.dados.loc[banco.current] = nova_linha
        banco.Atualiza()
        banco.Save()

        #MOSTRA MENSAGEM DE SUCESSO
        messagebox.showinfo(title="SUCESSO!", message="Atendimento Cadastrado com Sucesso!")

        #LIMPA AS SELEÇÕES E TEXTOS
        localEntry.delete(0,END)
        solEntry.delete(0,END)
        atendEntry.delete(0,END)
        certEntry.delete(0,END)
        chkValueMeta.set(False)
        chkValueResol.set(False)
        
        #ALTERA A QUANTIDADE DE ATENDIMENTOS
        qtd_atendimentos = banco.current 
        qtd['text'] = qtd_atendimentos
        qtd.place(relx=0.5, rely=0.5,anchor=CENTER)

        #ALTERA A LISTAGEM
        listagem.insert('', 'end', values=tuple(banco.dados.loc[qtd_atendimentos-1]))
        listagem.pack(side=LEFT)
    else:
        #CASO DE ERRADO
        Mensagem_Aviso(txt)

def Mostrar(event):
    
    try:
        global listagem, lista_atendimentos,lista_certificados,lista_locais,lista_solicitantes
        nodeId_1 = listagem.focus()
        
        id_ = listagem.item(nodeId_1)['values'][0]
        local = listagem.item(nodeId_1)['values'][1]
        solicitante = listagem.item(nodeId_1)['values'][2]
        atendimento = listagem.item(nodeId_1)['values'][3]
        certificado = listagem.item(nodeId_1)['values'][4]
        meta = listagem.item(nodeId_1)['values'][5]
        resolvido = listagem.item(nodeId_1)['values'][6]
        data = listagem.item(nodeId_1)['values'][7]
        condition = "Local == '{}' & Solicitante == '{}' & Atendimento == '{}' & Certificado == '{}' & Meta == '{}' & Resolvido == '{}' & Data == '{}' & Id == '{}'".format(local,solicitante,atendimento,certificado,meta,resolvido,data,str(id_))
        
        mostrar_jan = Tk()

        #CONFIGURACOES ----
        #Titulo
        mostrar_jan.title(titulos)
        #Tamanho da mostrar_janela
        mostrar_jan.geometry("500x450")
        #Cor de Fundo
        mostrar_jan.configure(background = cor)
        #Nao redimensionar
        mostrar_jan.resizable(width = False, height = False)
        #Transparencia
        mostrar_jan.attributes("-alpha",0.95)
        #Icone
        mostrar_jan.iconbitmap(default="Icons/icon.ico")
        cor_more = 'grey8'
        x_l = 40
        x_e = 200
        y_i = 30

        localLabel_ = Label(mostrar_jan,text="Local: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor)
        localLabel_.place(x=x_l, y = y_i)
        localEntry_ = Label(mostrar_jan,text=local,font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_more)
        localEntry_.place(x=x_e, y = y_i)
        solLabel_ = Label(mostrar_jan,text ="Solicitante: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor)
        solLabel_.place(x=x_l, y = y_i+50)
        solEntry_ = Label(mostrar_jan,text=solicitante,font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_more)
        solEntry_.place(x=x_e, y = y_i+50)
        atendLabel_ = Label(mostrar_jan,text="Atendiemento: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor)
        atendLabel_.place(x=x_l, y = y_i+100)
        atendEntry_ = Label(mostrar_jan,text = atendimento,font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_more)
        atendEntry_.place(x=x_e, y = y_i+100)
        certLabel_ = Label(mostrar_jan,text="Certificado: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor)
        certLabel_.place(x=x_l, y = y_i+150)
        certEntry_ = Label(mostrar_jan,text = certificado,font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_more)
        certEntry_.place(x=x_e, y = y_i+150)
        metaLabel_ = Label(mostrar_jan,text="Dispositivo Meta: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor)
        metaLabel_.place(x=x_l, y = y_i+200)
        meta_Entry_ = Label(mostrar_jan,text=meta,font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_more)
        meta_Entry_.place(x=x_e, y = y_i+200)
        resolv_Label_ = Label(mostrar_jan,text="Resolvido: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor)
        resolv_Label_.place(x=x_l, y = y_i+250)
        resolv_Entry_ = Label(mostrar_jan,text = resolvido,font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_more)
        resolv_Entry_.place(x=x_e, y = y_i+250)
        data_Label_ = Label(mostrar_jan,text="Data: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor)
        data_Label_.place(x=x_l, y = y_i+300)
        data_Entry_ = Label(mostrar_jan,text = data,font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor_more)
        data_Entry_.place(x=x_e, y = y_i+300)

        def Excluir():
            global listagem
            banco = Banco()

            x = banco.dados.query("Id == {} ".format(id_))


            banco.dados = banco.dados.drop(x.index)
            banco.Atualiza()
            
            qtd_atendimentos = banco.current 
            qtd['text'] = qtd_atendimentos
            
            listagem.delete(nodeId_1)
            listagem.pack(side=LEFT)
            
            banco.Save()
            messagebox.showinfo(title="Sucesso!", message="Cadastro Removido com Sucesso!")
            mostrar_jan.destroy()
        
        def Alterar():

            localEntry_ = AutocompleteCombobox(mostrar_jan,font=fonte_Textos, width=15)
            localEntry_.set_completion_list(lista_locais)
            localEntry_.place(x=x_e, y = y_i)
            
            solEntry_ = AutocompleteCombobox(mostrar_jan,font=fonte_Textos, width=15)
            solEntry_.set_completion_list(lista_solicitantes)
            solEntry_.place(x=x_e, y = y_i+50)
            
            atendEntry_ = AutocompleteCombobox(mostrar_jan,font=fonte_Textos, width=15)
            atendEntry_.set_completion_list(lista_atendimentos)
            atendEntry_.place(x=x_e, y = y_i+100)
            
            certEntry_ = AutocompleteCombobox(mostrar_jan,font=fonte_Textos, width=15)
            certEntry_.set_completion_list(lista_certificados)
            certEntry_.place(x=x_e, y = y_i+150)
            
            meta_Entry_ = AutocompleteCombobox(mostrar_jan,font=fonte_Textos, width=15)
            meta_Entry_.set_completion_list(["SIM","NÃO"])
            meta_Entry_.place(x=x_e, y = y_i+200)
            
            resolv_Entry_ = AutocompleteCombobox(mostrar_jan,font=fonte_Textos, width=15)
            resolv_Entry_.set_completion_list(["SIM","NÃO"])
            resolv_Entry_.place(x=x_e, y = y_i+250)
            
            data_Entry_ = Label(mostrar_jan,text = data, font=fonte_Textos,  fg=cor_contraste, bg=cor_more)
            data_Entry_.place(x=x_e, y = y_i+300)

            banco = Banco()
            x = banco.dados.query(condition)

            def Aplicar_Mudancas():
                
                local = localEntry_.get().upper()
                banco.dados["Local"][x.index[0]] = local
                solicitante = solEntry_.get().upper()
                banco.dados["Solicitante"][x.index[0]] = solicitante
                atendimento = atendEntry_.get().upper()
                banco.dados["Atendimento"][x.index[0]] = atendimento
                certificado = certEntry_.get().upper()
                banco.dados["Certificado"][x.index[0]] = certificado
                meta != meta_Entry_.get().upper()
                banco.dados["Meta"][x.index[0]] = meta 
                resolvido != resolv_Entry_.get().upper()
                banco.dados["Resolvido"][x.index[0]] = resolvido

                banco.Atualiza()
                banco.Save()
                
                listagem.delete(nodeId_1)
                listagem.insert('', 'end', values=(id_,local,solicitante,atendimento,certificado,meta,resolvido,data))
                listagem.pack(side=LEFT)

                messagebox.showinfo(title="Sucesso!", message="Cadastro Atualizado com Sucesso!")

            ex_button["text"] = "Aplicar"
            ex_button["comman"] = Aplicar_Mudancas

        alt_button = Button(mostrar_jan, text="Alterar", width = 20,bg=cor, fg=cor_contraste,relief="raise", command=Alterar)
        alt_button.place(x=x_l, y = y_i+350)
        ex_button = Button(mostrar_jan,text="Excluir" , width = 20,bg=cor, fg=cor_contraste,relief="raise",command=Excluir)
        ex_button.place(x=x_e+100,y = y_i+350)

        mostrar_jan.mainloop()
    except:
        pass
    

def Visualizar():
    pass
def Sobre():
    messagebox.showinfo(title="SOBRE",message="Software para controle de Suporte\n2021\nMeta Certificado Digital")

#BARRA DE MENUS
menubar = Menu(jan)

#MENU OPCOES
opmenu = Menu(menubar,tearoff=0)
opmenu.add_command(label="Visualizar Atendimentos",command=Visualizar)
menubar.add_cascade(label = "Opções", menu = opmenu)
#MENUN SOBRE
sobremenu = Menu(menubar,tearoff=0)
sobremenu.add_command(label="Sobre", command=Sobre)
menubar.add_cascade(label = "?", menu = sobremenu)

#TITULO
TopFrame = Frame(jan, width = largura, height = 100, bg = cor, relief = "raise" )
TopFrame.pack(side=TOP)

#Logo da Meta e Titulo do programa
logo_meta = Label(TopFrame, image=logo,bg=cor)
logo_meta.place(x=5,y=5)
meta = Label(TopFrame,text = "Controle de Atendimentos",font=fonte_Titulos, fg= cor_contraste, bg=cor)
meta.place(x=280,y=25)

#AMBIENTE DE INFORMACOES 1
infosFrame = Frame(jan, width = 450, height = 150, bg=cor,relief="raise")
infosFrame.place(x = 540,y=150)

#Data 
date = Label(infosFrame,text=data,fg=cor_contraste,bg=cor,font=fonte_Destaques)
date.place(x=140,y=5)

#Quantidade de Atendimentos
n_atendiLabel = Label(infosFrame, text="Atendimentos Realizados", fg = cor_contraste, bg=cor, font=fonte_Textos)
n_atendiLabel.place(x=125,y=50)
frame_aux = Frame(infosFrame, width = 200, height = 50, bg = "grey8", relief="raise")
frame_aux.place(x=125, y=85)
qtd = Label(frame_aux,text=qtd_atendimentos, bg = 'grey8' , fg="red", font=fonte_Destaques)
qtd.place(relx=0.5, rely=0.5,anchor=CENTER)

#AMBIENTE DE INFORMACOES 2
infos_2Frame = Frame(jan, width = 450, height = 225, bg=cor,relief="raise")
infos_2Frame.place(x = 540,y=325)

#VISUALIZACAO RAPIDA DE CADASTROS 
dadosCols = tuple(banco.dados.columns)
listagem = ttk.Treeview(infos_2Frame,columns = dadosCols, show='headings', height = 10)

listagem.bind('<Double-1>',Mostrar)

listagem.column("Id", width = 25)
listagem.heading("Id",text="ID")

listagem.column("Local", width = 70)
listagem.heading("Local",text="Local")

listagem.column("Solicitante", width = 70)
listagem.heading("Solicitante",text="Solicitante")

listagem.column("Atendimento", width = 70)
listagem.heading("Atendimento",text="Atendimento")

listagem.column("Certificado", width = 70)
listagem.heading("Certificado",text="Certificado")

listagem.column("Meta", width = 35)
listagem.heading("Meta",text="Meta")

listagem.column("Resolvido", width = 35)
listagem.heading("Resolvido",text="Resolvido")

listagem.column("Data", width = 70)
listagem.heading("Data",text="Data")

listagem.pack(side=LEFT)

#BARRAS DE ROLAGEM DA VISUALIZACAO
ysb = ttk.Scrollbar(infos_2Frame, orient=VERTICAL, command=listagem.yview)
listagem['yscroll'] = ysb.set
ysb.pack(side = RIGHT, fill = Y)

# TEXTOS DOS CABEÇALHO
for c in dadosCols:
    listagem.heading(c, text=c.title())

# INSRINDO OS ITENS
for item in dados.values:
    listagem.insert('', 'end', values=tuple(item))

#AMBIENTE DE CADASTRO
cadastroFrame = Frame(jan, width = 450, height = altura-200, bg=cor,relief="raise")
cadastroFrame.place(x = 40,y=150)

#LOCAL
localLabel = Label(cadastroFrame,text = "Local: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor)
localLabel.place(x = xLabels,y = yInicialCadastro )
localEntry = AutocompleteCombobox(cadastroFrame, width = entrysWidth)
lista_locais = list(banco.dados["Local"].drop_duplicates())
localEntry.set_completion_list(lista_locais)
localEntry.place(x = xEntrys, y = yInicialCadastro)

#SOLICITANTE
solLabel = Label(cadastroFrame,text = "Solicitante: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor)
solLabel.place(x = xLabels,y =yInicialCadastro + 70 )
solEntry = AutocompleteCombobox(cadastroFrame, width = entrysWidth)
solEntry.set_completion_list(lista_solicitantes)
solEntry.place(x = xEntrys, y = yInicialCadastro + 70 )

#ATENDIMENTO
atendLabel = Label(cadastroFrame,text = "Atendimento: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor)
atendLabel.place(x = xLabels,y = yInicialCadastro + 140 )
atendEntry = AutocompleteCombobox(cadastroFrame, width = entrysWidth)
atendEntry.set_completion_list(lista_atendimentos)
atendEntry.place(x = xEntrys, y = yInicialCadastro + 140 )

#CERTIFICADO
certLabel = Label(cadastroFrame,text = "Certificado: ",font=fonte_Textos, anchor="w", fg=cor_contraste, bg=cor)
certLabel.place(x = xLabels,y = yInicialCadastro + 210 )
certEntry = AutocompleteCombobox(cadastroFrame, width = entrysWidth)
certEntry.set_completion_list(lista_certificados)
certEntry.place(x = xEntrys, y = yInicialCadastro + 210 )

#META
chkValueMeta = BooleanVar() 
chkValueMeta.set(False)
chkMeta = Checkbutton(cadastroFrame, text='Dispostivo da Meta',var = chkValueMeta,bg=cor, activebackground = cor, fg=cor_contraste, selectcolor= cor)
chkMeta.place(x= xLabels,y = yInicialCadastro + 260)

#RESOLVIDO
chkValueResol = BooleanVar() 
chkValueResol.set(False)
chkResolv = Checkbutton(cadastroFrame, text='Problema Resolvido',var = chkValueResol,bg=cor, activebackground = cor, fg=cor_contraste, selectcolor = cor)
chkResolv.place(x = xEntrys + 100 ,y = yInicialCadastro + 260 )


#BOTAO DE INSERIR
cadastroButton = Button(cadastroFrame, text = "Inserir Atendimento", bg=cor, fg=cor_contraste, width = entrysWidth,command = Inserir)
cadastroButton.place(x = xEntrys - 50, y = yInicialCadastro + 300)

#LOOP PARA O APP FUNCIONAR
jan.config(menu = menubar)
jan.mainloop()