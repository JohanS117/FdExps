import tkinter as tk
from views.login_view import LoginView
from views.cliente_view import ClienteView
from views.restaurante_view import RestauranteView
from views.repartidor_view import RepartidorView

class FoodExpressApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FoodExpress - Comida a tu alcance")
        self.root.geometry("1300x800")
        self.root.configure(bg='#f8f9fa')
        
        self.usuario_actual = None
        self.usuario_nombre = None
        self.usuario_tipo = None
        
        self.mostrar_login()
    
    def mostrar_login(self):
        LoginView(self.root, self.on_login_success)
    
    def on_login_success(self, usuario_id, nombre, tipo):
        self.usuario_actual = usuario_id
        self.usuario_nombre = nombre
        self.usuario_tipo = tipo
        
        if tipo == 'cliente':
            ClienteView(self.root, self.usuario_actual, self.usuario_nombre, self.logout)
        elif tipo == 'restaurante':
            RestauranteView(self.root, self.usuario_actual, self.usuario_nombre, self.logout)
        else:
            RepartidorView(self.root, self.usuario_actual, self.usuario_nombre, self.logout)
    
    def logout(self):
        self.usuario_actual = None
        self.usuario_nombre = None
        self.usuario_tipo = None
        self.mostrar_login()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FoodExpressApp()
    app.run()