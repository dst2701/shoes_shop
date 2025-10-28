import tkinter as tk
from views.login_view import LoginView
from views.product_view import ProductView
from views.cart_view import CartView
from views.invoice_view import InvoiceView
from views.invoice_history_view import InvoiceHistoryView

class ShoesShopApp:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_root()

        # Initialize views
        self.login_view = LoginView(self.root)
        self.product_view = ProductView(self.root)
        self.cart_view = CartView(self.root)
        self.invoice_view = InvoiceView(self.root)
        self.invoice_history_view = InvoiceHistoryView(self.root)

        # Set up callbacks between views
        self.setup_callbacks()

    def setup_root(self):
        """Setup root window properties"""
        icon = tk.PhotoImage(file=r'd:\codeptit\Python\bangiay\image.png')
        self.root.iconphoto(True, icon)
        self.root.configure(bg='#ecf0f1')
        self.root.resizable(True, True)
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)

    def setup_callbacks(self):
        """Setup callbacks between different views"""
        # Login view callbacks
        self.login_view.set_login_callback(self.on_login_success)

        # Product view callbacks
        self.product_view.set_show_cart_callback(self.show_cart)
        self.product_view.set_show_invoice_history_callback(self.show_invoice_history)
        self.product_view.set_logout_callback(self.logout)

        # Cart view callbacks
        self.cart_view.set_logout_callback(self.logout)

        # Invoice view callbacks
        self.invoice_view.set_show_products_callback(self.show_products)

    def on_login_success(self, role, username):
        """Handle successful login"""
        self.current_role = role
        self.current_username = username
        self.product_view.show_shoes(role, username)

    def show_products(self, role, username):
        """Show products page"""
        self.product_view.show_shoes(role, username)

    def show_cart(self, username, role):
        """Show cart page"""
        self.cart_view.show_cart(username, role, self.show_products)

    def show_invoice_history(self, role, username):
        """Show invoice history page"""
        self.invoice_history_view.show(role, username, self.show_products)

    def logout(self):
        """Handle logout"""
        self.current_role = None
        self.current_username = None
        self.login_view.show_login()

    def toggle_fullscreen(self, event=None):
        """Toggle between full screen and window mode"""
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)

        # Return to normal size if exiting fullscreen
        if current_state:
            if self.root.title().startswith("Shop Shoes - Đăng nhập"):
                self.root.geometry("720x720")
            elif self.root.title().startswith("Shop Shoes - Đăng ký"):
                self.root.geometry("720x900")
            elif self.root.title().startswith("Shop Shoes - Danh sách"):
                self.root.geometry("1200x750")
            elif self.root.title().startswith("Shop Shoes - Giỏ hàng"):
                self.root.geometry("1000x700")
            elif self.root.title().startswith("Shop Shoes - Hóa đơn"):
                self.root.geometry("1000x800")

    def exit_fullscreen(self, event=None):
        """Exit fullscreen when Escape is pressed"""
        self.root.attributes('-fullscreen', False)
        # Return to normal sizes
        if self.root.title().startswith("Shop Shoes - Đăng nhập"):
            self.root.geometry("720x720")
        elif self.root.title().startswith("Shop Shoes - Đăng ký"):
            self.root.geometry("720x900")
        elif self.root.title().startswith("Shop Shoes - Danh sách"):
            self.root.geometry("1200x750")
        elif self.root.title().startswith("Shop Shoes - Giỏ hàng"):
            self.root.geometry("1000x700")
        elif self.root.title().startswith("Shop Shoes - Hóa đơn"):
            self.root.geometry("1000x800")

    def run(self):
        """Start the application"""
        self.login_view.show_login()
        self.root.mainloop()

if __name__ == "__main__":
    app = ShoesShopApp()
    app.run()
