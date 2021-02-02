from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

Courier = ('Courier',17,'bold')
class Atm:
    def __init__(self,main):
        
        self.cont = 0
        self.conn = sqlite3.connect('atm.db',timeout=100)
        self.login = False
        self.main = main
        self.top = Label(self.main,text='Banco el progreso',bg='#1f1c2c',fg='white',font=('Courier',30,'bold'))
        self.top.pack(fill=X)
        self.frame = Frame(self.main,bg='#2193b0',width=600,height=500)
        
        
        self.account = Label(self.frame,text='Numero de cuenta',bg="#728B8E",fg="white",font=Courier)
        self.last = Button(self.frame,text='Ultima transaccion',bg='#1f1c2c',fg='white',font=('Courier',8,'bold'),command=self.history)
        self.accountEntry = Entry(self.frame,bg='#FFFFFF',highlightcolor="#50A8B0", highlightthickness=2, highlightbackground="white")
        self.pin = Label(self.frame,text='contraseña',bg="#728B8E",fg="white",font=Courier)
        self.pinEntry = Entry(self.frame,show='*',bg='#FFFFFF',highlightcolor="#50A8B0", highlightthickness=2, highlightbackground="white")
        self.button = Button(self.frame,text='Ingresar',bg='#1f1c2c',fg='white',font=('Courier',20,'bold'),command=self.validate)
        self.quit = Button(self.frame,text='Salir',bg='#1f1c2c',fg='white',font=('Courier',20,'bold'),command=self.main.destroy)
        self.pinAtm = Entry(self.frame,show='*',bg='#FFFFFF',highlightcolor="#50A8B0", highlightthickness=2, highlightbackground="white")
        
        self.pinAtm.place(x=50,y=370,width=140,height=25)
        self.last.place(x=50,y=400,width=140,height=30)
        self.account.place(x=45,y=100,width=220,height=20)
        self.accountEntry.place(x=325,y=97,width=200,height=25)
        self.pin.place(x=45,y=180,width=220,height=20)
        self.pinEntry.place(x=325,y=180,width=200,height=25)
        self.button.place(x=240,y=260,width=150,height=30)
        self.quit.place(x=400,y=400,width=100,height=30)
        self.frame.pack()

    def fetch(self):
        self.list = []
        self.details = self.conn.execute('Select nom_dueño, pass, id_cuenta, tipo, balance, estado from cuenta where id_cuenta = ?',(self.ac,))
        for i in self.details:
            self.list.append('Nombre:  {}'.format(i[0]))
            self.list.append('Numero de cuenta: {}'.format(i[2]))
            self.list.append('Tipo cuenta:= {}'.format(i[3]))
            self.ac = i[2]
            self.amo = i[4]
            self.list.append('Balance: COP${}'.format(i[4]))
            self.list.append('Estado: {}'.format(i[5]))

    def validate(self):
        ac = False
        self.details = self.conn.execute('Select nom_dueño, pass, id_cuenta, tipo, balance, estado from cuenta where id_cuenta= ?',(self.accountEntry.get(),))
        for i in self.details:
            self.ac = i[2]
            if i[2] == self.accountEntry.get():
                ac = True
            elif i[1] == int(self.pinEntry.get()):
                if (i[5] != "bloqueada"):
                    ac = True
                    m = 'Bienvenido {}!'.format(i[0])
                    self.fetch()
                    messagebox._show("Informacion", m)
                    cont = 0
                    self.frame.destroy()
                    self.menu()
                else:
                    messagebox._show("ALERTA","Su cuenta esta bloqueada")
                    return
            else:
                ac = True
                m = " Contraseña incorrecta "
                messagebox._show("Informacion", m)
                self.cont += 1
                if (self.cont==3):
                    messagebox._show("ALERTA", "Cuenta bloqueada, Máximo de intentos permitidos")
                    self.conn.execute('Update cuenta set estado = "bloqueada" where id_cuenta=?',(self.accountEntry.get()))
                    self.conn.commit()

            if not ac:
                m = " Numero de cuenta incorrecto "
                messagebox._show("Informacion", m)
                
    def menu(self):
        self.frame = Frame(self.main,bg='#2193b0',width=650 ,height=600)
        main.geometry('800x600')
        self.user_info = Button(self.frame,text='Información de la cuenta',bg='#1f1c2c',fg='white',font=('Courier',10,'bold'),command=self.account_details)
        self.balance_enquiry = Button(self.frame,text='Balance',bg='#1f1c2c',fg='white',font=('Courier',10,'bold'),command=self.check)
        self.deposit = Button(self.frame,text='Depositar',bg='#1f1c2c',fg='white',font=('Courier',10,'bold'),command=self.deposit)
        self.transfer = Button(self.frame,text='Trasferencia',bg='#1f1c2c',fg='white',font=('Courier',10,'bold'),command=self.transfer)
        self.withdraw = Button(self.frame,text='Retirar',bg='#1f1c2c',fg='white',font=('Courier',10,'bold'),command=self.withdraw)

        self.changePin = Button(self.frame,text='Cambiar Pin',bg='#1f1c2c',fg='white',font=('Courier',8,'bold'),command=self.change)

        self.quit = Button(self.frame, text='Salir', bg='#1f1c2c', fg='white', font=('Courier', 10, 'bold'),command=self.main.destroy)

        self.user_info.place(x=0,y=0,width=200,height=50)
        self.balance_enquiry.place(x=0,y=500,width=200,height=50)
        self.deposit.place(x=450,y=0,width=200,height=50)
        self.transfer.place(x=0,y=240,width=120,height=50)
        self.withdraw.place(x=450,y=500,width=200,height=50)
        self.changePin.place(x=530, y=240, width=130, height=50)
        self.quit.place(x=270,y=515,width=100,height=30)
        self.frame.pack()

    def account_details(self):
        self.entries()
        self.remove_change_pin()
        self.fetch()
        self.limpiar = Label(self.frame, text='', font=('Courier',20,'bold'))
        self.limpiar.place(x=140, y=180, width=380, height=180)
        display = self.list[0]+'\n'+self.list[1]+'\n'+self.list[2] +'\n'+ self.list[4] 
        self.label = Label(self.frame, text=display, font=('Courier',20,'bold'))
        self.label.place(x=140, y=180, width=380, height=180)

    def check(self):
        self.entries()
        self.remove_change_pin()
        self.fetch()
        b = self.list[3]
        self.label = Label(self.frame, text=b, font=('Courier',20,'bold'))
        self.label.place(x=140, y=180, width=380, height=250)

    def transfer(self):
        self.remove_change_pin()
        self.limpiar = Label(self.frame, text='', font=('Courier',20,'bold'))
        self.limpiar.place(x=140, y=180, width=380, height=250)
        self.label = Label(self.frame, text='Ingrese la cantidad a depositar:', font=('Courier', 10, 'bold'))
        self.label.place(x=140, y=200, width=300, height=30)
        self.label2 = Label(self.frame, text='Ingrese numero de cuenta destino:', font=('Courier', 10, 'bold'))
        self.label2.place(x=140, y=270, width=300, height=30)
        self.amount = Entry(self.frame,bg='#FFFFFF',highlightcolor="#50A8B0", highlightthickness=2, highlightbackground="white")
        self.submitButton = Button(self.frame,text='Trasnferir',bg='#1f1c2c',fg='white',font=('Courier',10,'bold'))
        self.amount2 = Entry(self.frame,bg='#FFFFFF',highlightcolor="#50A8B0", highlightthickness=2, highlightbackground="white")


        self.amount.place(x=230,y=240,width=160,height=20)
        self.amount2.place(x=230,y=310,width=160,height=20)

        self.submitButton.place(x=250,y=350,width=100,height=20)
        self.submitButton.bind("<ButtonRelease-1>",self.tranfer_trans)
        
    def tranfer_trans(self,flag):
        if(self.amount.get()=='' or self.amount2.get()==''):
            d = 'Ingrese los campos correctamente'
            messagebox._show('Error transaccional',d)
        elif int(self.amo) < int(self.amount.get()):
            d = 'Monto supera el balance de la cuenta'
            messagebox._show('Error transaccional',d)            
        else:
            aux = False
            details = self.conn.execute('Select nom_dueño, pass, id_cuenta, tipo, balance, estado from cuenta where id_cuenta= ?',(self.amount2.get(),))
            for i in details:
                aux = i[2]
            if not aux:
                m = " Numero de cuenta incorrecto "
                messagebox._show("Informacion", m)
            else:
                self.limpiar = Label(self.frame, text='', font=('Courier',20,'bold'))
                self.limpiar.place(x=140, y=180, width=380, height=180)
                self.label = Label(self.frame,text='Transaccion exitosa!',font=('Courier',10,'bold'))
                self.label.place(x=180, y=180, width=300, height=100)
                self.conn.execute('Update cuenta set balance = balance-? where id_cuenta=?',(self.amount.get(), self.ac))
                self.conn.execute('Update cuenta set balance = balance+? where id_cuenta=?',(self.amount.get(), self.amount2.get())) 
                self.conn.execute('Insert into transaccion (descripcion , estado , fecha , id_Cajero , id_Cuenta, monto, id_CuentaDestino) values ("Transferencia","aprobado","02/02/2021",1000, ? , ? , ? )',( self.ac , self.amount.get() , self.amount2.get()))
                self.conn.commit()
                self.entries()
                self.fetch()

    def deposit(self):
        self.limpiar = Label(self.frame, text='', font=('Courier',20,'bold'))
        self.limpiar.place(x=140, y=180, width=380, height=250)
        self.remove_change_pin()
        self.label = Label(self.frame, text='Ingrese la cantidad a depositar:', font=('Courier', 10, 'bold'))
        self.label.place(x=180, y=180, width=300, height=100)
        self.amount = Entry(self.frame,bg='#FFFFFF',highlightcolor="#50A8B0", highlightthickness=2, highlightbackground="white")
        self.submitButton = Button(self.frame,text='Depositar',bg='#1f1c2c',fg='white',font=('Courier',10,'bold'))

        self.amount.place(x=195,y=300,width=160,height=20)
        self.submitButton.place(x=365,y=300,width=100,height=20)
        self.submitButton.bind("<ButtonRelease-1>",self.deposit_trans)

    def deposit_trans(self,flag):
        if(self.amount.get()==''):
            d = 'Ingrese cantidad'
            messagebox._show('Error transaccional',d)
        else:
            self.limpiar = Label(self.frame, text='', font=('Courier',20,'bold'))
            self.limpiar.place(x=140, y=180, width=380, height=180)
            self.label = Label(self.frame,text='Transaccion exitosa!',font=('Courier',10,'bold'))
            self.label.place(x=180, y=180, width=300, height=100)
            self.conn.execute('Update cuenta set balance = balance+? where id_cuenta=?',(self.amount.get(),self.ac))
            self.conn.execute('Insert into transaccion (descripcion , estado , fecha , id_Cajero , id_Cuenta, monto) values ("Depositar","aprobado","02/02/2021",1000, ? , ?)',( self.ac , self.amount.get() ))
            self.conn.commit()
            self.write_deposit()
            self.entries()
            self.fetch()

    def write_deposit(self):
        self.last_deposit = 'Cantidad:{} Cuenta:{}'.format(self.amount.get(), self.list[1])
        f = open('ultima.txt', 'w')
        f.write(self.last_deposit)
        f.close()

    def withdraw(self):
        self.limpiar = Label(self.frame, text='', font=('Courier',20,'bold'))
        self.limpiar.place(x=140, y=180, width=380, height=250)
        self.remove_change_pin()
        self.label = Label(self.frame, text='Ingrese la cantidad a retirar', font=('Courier', 10, 'bold'))
        self.label.place(x=180, y=180, width=300, height=100)
        self.amount = Entry(self.frame, bg='#FFFFFF', highlightcolor="#50A8B0", highlightthickness=2,highlightbackground="white")
        self.submitButton = Button(self.frame, text='Retirar', bg='#1f1c2c', fg='white', font=('Courier', 10, 'bold'))
        self.amount.place(x=195, y=300, width=160, height=20)
        self.submitButton.place(x=365, y=300, width=100, height=20)
        self.submitButton.bind("<ButtonRelease-1>", self.with_trans)

    def with_trans(self,flag):
        if (self.amount.get() == ''):
            d = 'Enter amount'
            messagebox._show('Transaction Error', d)
        elif (self.amo < int(self.amount.get())):
            d = 'Monto supera el balance de la cuenta'
            messagebox._show('Error transaccional',d) 
        else:
            self.limpiar = Label(self.frame, text='', font=('Courier',20,'bold'))
            self.limpiar.place(x=140, y=180, width=380, height=180)
            self.label = Label(self.frame, text='Transaccion exitosa', font=('Courier', 10, 'bold'))
            self.label.place(x=180, y=180, width=300, height=100)
            self.conn.execute('Update cuenta set balance = balance-? where id_cuenta=?', (self.amount.get(), self.ac))
            self.conn.execute('Insert into transaccion (descripcion , estado , fecha , id_Cajero , id_Cuenta, monto) values ("Retiro","aprobado","02/02/2021",1000, ? , ?)',( self.ac , self.amount.get() ))
            self.conn.commit()
            self.last_with()
            self.entries()
            self.fetch()


    def last_with(self):
        self.last_withdraw = 'Cantidad:{} \n Cuenta:{}'.format(self.amount.get(), self.list[1])
        f = open('ultima.txt', 'w')
        f.write(self.last_withdraw)
        f.close()

    def change(self):
        self.limpiar = Label(self.frame, text='', font=('Courier',20,'bold'))
        self.limpiar.place(x=140, y=180, width=380, height=250)
 
        self.entries()
        self.label = Label(self.frame,text='Cambiar PIN',font=('Courier', 10, 'bold'))
        self.old = Entry(self.frame, bg='#FFFFFF', highlightcolor="#50A8B0", highlightthickness=2, highlightbackground="white")
        self.new = Entry(self.frame, bg='#FFFFFF', highlightcolor="#50A8B0", highlightthickness=2, highlightbackground="white")
        self.confirm = Entry(self.frame, bg='#FFFFFF', highlightcolor="#50A8B0", highlightthickness=2, highlightbackground="white")
        self.submit2 = Button(self.frame, text='Cambiar', bg='#1f1c2c', fg='white', font=('Courier', 10, 'bold'))

        self.old.insert(0, 'Contraseña antigua')
        self.old.bind('<FocusIn>',self.on_entry_click)
        self.new.insert(0, 'Nueva contraseña')
        self.new.bind('<FocusIn>', self.on_entry_click2)
        self.confirm.insert(0, 'Confirme nueva contraseña')
        self.confirm.bind('<FocusIn>', self.on_entry_click3)
        self.submit2.bind('<Button-1>',self.change_req)

        self.label.place(x=180, y=180, width=300, height=100)
        self.old.place(x=230, y=300, width=180, height=20)
        self.new.place(x=230, y=330, width=180, height=20)
        self.confirm.place(x=230, y=360, width=180, height=20)
        self.submit2.place(x=230, y=390, width=180, height=20)

    def change_req(self,flag):
        if(self.old.get()=='' or self.new.get()=='' or self.confirm.get()==''):
            messagebox._show('Intente llenar todos los campos')
        else:
            self.fetch()
            self.details = self.conn.execute('Select nom_dueño, pass, id_cuenta, tipo, balance, estado from cuenta where id_cuenta = ?',(self.ac,))
            for i in self.details:
                p = str(i[1])
            if self.old.get() == p:
                if self.new.get() == self.confirm.get():
                    self.limpiar = Label(self.frame, text='', font=('Courier',20,'bold'))
                    self.limpiar.place(x=140, y=180, width=380, height=250)
                    self.conn.execute('Update cuenta set pass = ? where id_cuenta=?', (self.new.get(), self.ac))
                    self.conn.commit()
                    messagebox._show("Pin actualizado","Contraseña actualizada")
                    self.remove_change_pin()
                    messagebox._show('Reinicio','Vuelva a ingresar')
                    main.destroy()

    def on_entry_click(self,event):
        self.entry = True
        if self.entry:
            self.entry = False
            self.old.delete(0,'end')
            self.old.insert(0,'')

    def on_entry_click2(self,event):
        self.entry = True
        if self.entry:
            self.entry = False
            self.new.delete(0,'end')
            self.new.insert(0,'')

    def on_entry_click3(self,event):
        self.entry = True
        if self.entry:
            self.entry = False
            self.confirm.delete(0,'end')
            self.confirm.insert(0,'')

    def history(self):
        flag = False
        details = self.conn.execute('Select Clave,Estado,Saldo from cajero where Clave = 1000')#, (self.pinAtm.get(),))
        for i in details:
            flag = i[0]
            print(flag)
    
        if not flag:
            messagebox._show("ALERTA","Clave del cajero incorrecta ")
        else:    
            self.entries()
            self.remove_change_pin()
            f = open('ultima.txt','r')
            self.hist = f.readlines()
            f.close()
            m = self.hist
            messagebox._show("Ultima transaccion", m)

    def entries(self):
        try:
            self.amount.place_forget()
            self.submitButton.place_forget()
        except:
            pass

    def remove_change_pin(self):
        try:
            self.old.place_forget()
            self.new.place_forget()
            self.confirm.place_forget()
            self.submit2.place_forget()
        except:
            pass

main = Tk()
main.title('Banco el progreso')
window_height = 500
window_width = 900

screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

main.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
main.resizable(width=False, height=False)
icon = PhotoImage(file='bank.png')
main.tk.call('wm','iconphoto',main._w,icon)
interface = Atm(main)
main.mainloop()
