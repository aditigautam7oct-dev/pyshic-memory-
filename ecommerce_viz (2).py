# E-commerce Store Management System - Complete with Visualization
# For BBA Students - Integrated System with Data Analytics

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import numpy as np

class EcommerceStoreComplete:
    def __init__(self):
        self.products = {}
        self.sales_history = []
        self.total_revenue = 0.0
        self.data_file = "store_data.json"
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("🛒 E-commerce Store Manager - Complete System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Load data
        self.load_data()
        
        # Setup GUI
        self.setup_gui()
    
    def load_data(self):
        """Load existing data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                    self.products = data.get('products', {})
                    self.sales_history = data.get('sales_history', [])
                    self.total_revenue = data.get('total_revenue', 0.0)
            except:
                pass
    
    def save_data(self):
        """Save current data to file"""
        data = {
            'products': self.products,
            'sales_history': self.sales_history,
            'total_revenue': self.total_revenue
        }
        try:
            with open(self.data_file, 'w') as file:
                json.dump(data, file, indent=2)
            messagebox.showinfo("Success", "Data saved successfully!")
        except:
            messagebox.showerror("Error", "Error saving data.")
    
    def setup_gui(self):
        """Setup the main GUI interface"""
        
        # Title Frame
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x', padx=5, pady=5)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🛒 E-COMMERCE STORE MANAGER", 
                              font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        # Dashboard Frame
        dashboard_frame = tk.Frame(self.root, bg='#f0f0f0')
        dashboard_frame.pack(fill='x', padx=5, pady=5)
        
        # Revenue Display
        self.revenue_frame = tk.Frame(dashboard_frame, bg='#27ae60', height=50)
        self.revenue_frame.pack(side='left', fill='both', expand=True, padx=2)
        
        self.revenue_label = tk.Label(self.revenue_frame, 
                                     text=f"💰 Revenue: ${self.total_revenue:.2f}", 
                                     font=('Arial', 12, 'bold'), fg='white', bg='#27ae60')
        self.revenue_label.pack(expand=True)
        
        # Products Count
        self.products_frame = tk.Frame(dashboard_frame, bg='#3498db', height=50)
        self.products_frame.pack(side='left', fill='both', expand=True, padx=2)
        
        self.products_label = tk.Label(self.products_frame, 
                                      text=f"📦 Products: {len(self.products)}", 
                                      font=('Arial', 12, 'bold'), fg='white', bg='#3498db')
        self.products_label.pack(expand=True)
        
        # Sales Count
        self.sales_frame = tk.Frame(dashboard_frame, bg='#e74c3c', height=50)
        self.sales_frame.pack(side='left', fill='both', expand=True, padx=2)
        
        self.sales_label = tk.Label(self.sales_frame, 
                                    text=f"🛍️ Sales: {len(self.sales_history)}", 
                                    font=('Arial', 12, 'bold'), fg='white', bg='#e74c3c')
        self.sales_label.pack(expand=True)
        
        # Button Frame
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(fill='x', padx=10, pady=5)
        
        buttons = [
            ("➕ Add Product", self.add_product_dialog, '#3498db'),
            ("📦 Update Stock", self.update_stock_dialog, '#f39c12'),
            ("❌ Remove", self.remove_product_dialog, '#e74c3c'),
            ("🛒 Process Order", self.process_order_dialog, '#2ecc71'),
            ("📊 Sales Report", self.show_sales_report, '#9b59b6'),
            ("⚠️ Low Stock", self.check_low_stock, '#e67e22'),
            ("📈 Analytics", self.show_visualizations, '#16a085'),
            ("💾 Save", self.save_data, '#34495e')
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(button_frame, text=text, command=command, 
                           font=('Arial', 9, 'bold'), fg='white', bg=color,
                           width=13, height=2, relief='flat')
            btn.grid(row=i//4, column=i%4, padx=3, pady=3, sticky='ew')
        
        for i in range(4):
            button_frame.columnconfigure(i, weight=1)
        
        # Inventory Frame
        inventory_frame = tk.LabelFrame(self.root, text="📋 Current Inventory", 
                                       font=('Arial', 12, 'bold'), bg='#f0f0f0')
        inventory_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('ID', 'Name', 'Price', 'Stock', 'Sold', 'Revenue')
        self.inventory_tree = ttk.Treeview(inventory_frame, columns=columns, show='headings', height=12)
        
        col_widths = {'ID': 100, 'Name': 200, 'Price': 100, 'Stock': 80, 'Sold': 80, 'Revenue': 120}
        for col in columns:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=col_widths[col], anchor='center')
        
        scrollbar = ttk.Scrollbar(inventory_frame, orient='vertical', command=self.inventory_tree.yview)
        self.inventory_tree.configure(yscrollcommand=scrollbar.set)
        
        self.inventory_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.update_inventory_display()
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready", 
                                  bd=1, relief='sunken', anchor='w', bg='#ecf0f1')
        self.status_bar.pack(side='bottom', fill='x')
        
        self.update_dashboard()
    
    def update_inventory_display(self):
        """Update the inventory treeview"""
        for item in self.inventory_tree.get_children():
            self.inventory_tree.delete(item)
        
        for product_id, product in self.products.items():
            revenue = product['price'] * product['total_sold']
            self.inventory_tree.insert('', 'end', values=(
                product_id,
                product['name'],
                f"${product['price']:.2f}",
                product['quantity'],
                product['total_sold'],
                f"${revenue:.2f}"
            ))
    
    def update_dashboard(self):
        """Update dashboard displays"""
        self.revenue_label.config(text=f"💰 Revenue: ${self.total_revenue:.2f}")
        self.products_label.config(text=f"📦 Products: {len(self.products)}")
        self.sales_label.config(text=f"🛍️ Sales: {len(self.sales_history)}")
        
        total_items = sum(p['quantity'] for p in self.products.values())
        self.status_bar.config(text=f"Ready | Products: {len(self.products)} | Stock: {total_items}")
    
    def add_product_dialog(self):
        """Dialog to add new product"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Product")
        dialog.geometry("400x300")
        dialog.configure(bg='#f0f0f0')
        dialog.grab_set()
        
        tk.Label(dialog, text="Add New Product", font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=10)
        
        fields = [
            ("Product ID:", tk.StringVar()),
            ("Product Name:", tk.StringVar()),
            ("Price ($):", tk.StringVar()),
            ("Initial Stock:", tk.StringVar())
        ]
        
        entries = {}
        for label_text, var in fields:
            frame = tk.Frame(dialog, bg='#f0f0f0')
            frame.pack(fill='x', padx=20, pady=5)
            tk.Label(frame, text=label_text, width=15, anchor='w', bg='#f0f0f0').pack(side='left')
            entry = tk.Entry(frame, textvariable=var, width=25)
            entry.pack(side='right')
            entries[label_text] = var
        
        def add_product():
            try:
                product_id = entries["Product ID:"].get().strip()
                name = entries["Product Name:"].get().strip()
                price = float(entries["Price ($):"].get())
                quantity = int(entries["Initial Stock:"].get())
                
                if not product_id or not name:
                    messagebox.showerror("Error", "Please fill all fields!")
                    return
                
                if product_id in self.products:
                    messagebox.showerror("Error", f"Product {product_id} already exists!")
                    return
                
                self.products[product_id] = {
                    'name': name,
                    'price': price,
                    'quantity': quantity,
                    'total_sold': 0
                }
                
                self.update_inventory_display()
                self.update_dashboard()
                messagebox.showinfo("Success", f"Product '{name}' added!")
                dialog.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Invalid input!")
        
        button_frame = tk.Frame(dialog, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Add", command=add_product, 
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold'), width=10).pack(side='left', padx=10)
        tk.Button(button_frame, text="Cancel", command=dialog.destroy, 
                 bg='#95a5a6', fg='white', font=('Arial', 10, 'bold'), width=10).pack(side='left')
    
    def update_stock_dialog(self):
        """Update product stock"""
        if not self.products:
            messagebox.showwarning("Warning", "No products available!")
            return
        
        product_id = simpledialog.askstring("Update Stock", "Enter Product ID:")
        if not product_id or product_id not in self.products:
            messagebox.showerror("Error", "Product not found!")
            return
        
        new_quantity = simpledialog.askinteger("Update Stock", 
                                              f"Current: {self.products[product_id]['quantity']}\nNew quantity:")
        if new_quantity is not None and new_quantity >= 0:
            self.products[product_id]['quantity'] = new_quantity
            self.update_inventory_display()
            self.update_dashboard()
            messagebox.showinfo("Success", "Stock updated!")
    
    def remove_product_dialog(self):
        """Remove product"""
        if not self.products:
            messagebox.showwarning("Warning", "No products!")
            return
        
        product_id = simpledialog.askstring("Remove Product", "Enter Product ID:")
        if not product_id or product_id not in self.products:
            messagebox.showerror("Error", "Product not found!")
            return
        
        name = self.products[product_id]['name']
        if messagebox.askyesno("Confirm", f"Remove '{name}'?"):
            del self.products[product_id]
            self.update_inventory_display()
            self.update_dashboard()
            messagebox.showinfo("Success", f"'{name}' removed!")
    
    def process_order_dialog(self):
        """Process customer order"""
        if not self.products:
            messagebox.showwarning("Warning", "No products!")
            return
        
        product_id = simpledialog.askstring("Process Order", "Enter Product ID:")
        if not product_id or product_id not in self.products:
            messagebox.showerror("Error", "Product not found!")
            return
        
        product = self.products[product_id]
        quantity = simpledialog.askinteger("Process Order", 
                                          f"Product: {product['name']}\nPrice: ${product['price']:.2f}\n"
                                          f"Available: {product['quantity']}\n\nQuantity:")
        
        if quantity is None or quantity <= 0:
            return
        
        if product['quantity'] < quantity:
            messagebox.showerror("Error", f"Insufficient stock! Available: {product['quantity']}")
            return
        
        total_price = product['price'] * quantity
        product['quantity'] -= quantity
        product['total_sold'] += quantity
        
        sale_record = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'product_id': product_id,
            'product_name': product['name'],
            'quantity': quantity,
            'unit_price': product['price'],
            'total_amount': total_price
        }
        
        self.sales_history.append(sale_record)
        self.total_revenue += total_price
        
        self.update_inventory_display()
        self.update_dashboard()
        
        messagebox.showinfo("Success", 
                           f"Product: {product['name']}\n"
                           f"Quantity: {quantity}\n"
                           f"Total: ${total_price:.2f}\n"
                           f"Remaining: {product['quantity']}")
    
    def show_sales_report(self):
        """Show sales report"""
        if not self.sales_history:
            messagebox.showinfo("Sales Report", "No sales yet!")
            return
        
        report_window = tk.Toplevel(self.root)
        report_window.title("📊 Sales Report")
        report_window.geometry("700x500")
        report_window.configure(bg='#f0f0f0')
        
        header = tk.Frame(report_window, bg='#34495e')
        header.pack(fill='x', padx=5, pady=5)
        tk.Label(header, text="📊 SALES REPORT", 
                font=('Arial', 14, 'bold'), fg='white', bg='#34495e').pack(pady=10)
        
        summary = tk.Frame(report_window, bg='#f0f0f0')
        summary.pack(fill='x', padx=10, pady=10)
        
        total_items = sum(sale['quantity'] for sale in self.sales_history)
        avg_sale = self.total_revenue / len(self.sales_history)
        
        tk.Label(summary, text=f"Transactions: {len(self.sales_history)}", 
                font=('Arial', 11), bg='#f0f0f0').pack(anchor='w')
        tk.Label(summary, text=f"Revenue: ${self.total_revenue:.2f}", 
                font=('Arial', 11, 'bold'), fg='#27ae60', bg='#f0f0f0').pack(anchor='w')
        tk.Label(summary, text=f"Items Sold: {total_items}", 
                font=('Arial', 11), bg='#f0f0f0').pack(anchor='w')
        tk.Label(summary, text=f"Avg Sale: ${avg_sale:.2f}", 
                font=('Arial', 11), bg='#f0f0f0').pack(anchor='w')
        
        list_frame = tk.Frame(report_window)
        list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('Date', 'Product', 'Qty', 'Amount')
        sales_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        for col, width in zip(columns, [150, 200, 80, 100]):
            sales_tree.heading(col, text=col)
            sales_tree.column(col, width=width, anchor='center' if col in ['Qty', 'Amount'] else 'w')
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=sales_tree.yview)
        sales_tree.configure(yscrollcommand=scrollbar.set)
        
        for sale in reversed(self.sales_history[-50:]):
            sales_tree.insert('', 0, values=(
                sale['date'],
                sale['product_name'],
                sale['quantity'],
                f"${sale['total_amount']:.2f}"
            ))
        
        sales_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def check_low_stock(self):
        """Check low stock"""
        threshold = simpledialog.askinteger("Low Stock", "Threshold:", initialvalue=5)
        if threshold is None:
            return
        
        low_stock = [f"{pid}: {p['name']} (Stock: {p['quantity']})"
                     for pid, p in self.products.items() if p['quantity'] <= threshold]
        
        if low_stock:
            messagebox.showwarning("Low Stock", f"⚠️ Low Stock (≤{threshold}):\n\n" + "\n".join(low_stock))
        else:
            messagebox.showinfo("Stock Status", "✅ All products have sufficient stock!")
    
    def show_visualizations(self):
        """Show comprehensive visualizations using matplotlib, pandas, numpy"""
        if not self.products and not self.sales_history:
            messagebox.showinfo("Analytics", "No data available!")
            return
        
        viz_window = tk.Toplevel(self.root)
        viz_window.title("📈 Business Analytics Dashboard")
        viz_window.geometry("1400x900")
        viz_window.configure(bg='#f0f0f0')
        
        header = tk.Frame(viz_window, bg='#2c3e50', height=50)
        header.pack(fill='x')
        header.pack_propagate(False)
        tk.Label(header, text="📈 BUSINESS ANALYTICS DASHBOARD", 
                font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50').pack(expand=True)
        
        notebook = ttk.Notebook(viz_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.create_inventory_analytics(notebook)
        self.create_sales_analytics(notebook)
        self.create_performance_analytics(notebook)
        self.create_financial_analytics(notebook)
    
    def create_inventory_analytics(self, notebook):
        """Inventory analytics with numpy, pandas, matplotlib"""
        tab = tk.Frame(notebook, bg='white')
        notebook.add(tab, text='📦 Inventory Analytics')
        
        if not self.products:
            tk.Label(tab, text="No inventory data", font=('Arial', 14)).pack(expand=True)
            return
        
        fig = Figure(figsize=(14, 8), facecolor='white', dpi=100)
        
        # Prepare data using pandas
        product_data = pd.DataFrame([
            {
                'id': pid,
                'name': p['name'],
                'price': p['price'],
                'quantity': p['quantity'],
                'sold': p['total_sold'],
                'value': p['price'] * p['quantity'],
                'revenue': p['price'] * p['total_sold']
            }
            for pid, p in self.products.items()
        ])
        
        # Chart 1: Stock Levels Bar Chart
        ax1 = fig.add_subplot(2, 2, 1)
        names = [n[:15] for n in product_data['name']]
        stocks = product_data['quantity'].values
        
        # Color coding using numpy
        colors = np.where(stocks > 10, '#2ecc71', np.where(stocks > 5, '#f39c12', '#e74c3c'))
        
        bars = ax1.bar(range(len(names)), stocks, color=colors, alpha=0.8, edgecolor='black', linewidth=1.2)
        ax1.set_xlabel('Products', fontweight='bold', fontsize=10)
        ax1.set_ylabel('Stock Quantity', fontweight='bold', fontsize=10)
        ax1.set_title('Current Stock Levels by Product', fontweight='bold', fontsize=12, pad=15)
        ax1.set_xticks(range(len(names)))
        ax1.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
        ax1.grid(axis='y', alpha=0.3, linestyle='--')
        
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        # Chart 2: Inventory Value Pie Chart
        ax2 = fig.add_subplot(2, 2, 2)
        values = product_data['value'].values
        
        if values.sum() > 0:
            wedges, texts, autotexts = ax2.pie(values, labels=names, autopct='%1.1f%%',
                                               startangle=90, colors=plt.cm.Pastel1.colors,
                                               explode=[0.05] * len(names))
            for text in texts:
                text.set_fontsize(8)
            for autotext in autotexts:
                autotext.set_color('black')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(8)
            
            ax2.set_title('Inventory Value Distribution ($)', fontweight='bold', fontsize=12, pad=15)
        
        # Chart 3: Stock vs Sold Comparison
        ax3 = fig.add_subplot(2, 2, 3)
        x = np.arange(len(names))
        width = 0.35
        
        bars1 = ax3.bar(x - width/2, product_data['quantity'], width, 
                       label='Current Stock', color='#3498db', alpha=0.8, edgecolor='black')
        bars2 = ax3.bar(x + width/2, product_data['sold'], width, 
                       label='Total Sold', color='#e74c3c', alpha=0.8, edgecolor='black')
        
        ax3.set_xlabel('Products', fontweight='bold', fontsize=10)
        ax3.set_ylabel('Quantity', fontweight='bold', fontsize=10)
        ax3.set_title('Stock vs Sales Comparison', fontweight='bold', fontsize=12, pad=15)
        ax3.set_xticks(x)
        ax3.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
        ax3.legend(loc='upper right', fontsize=9)
        ax3.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Chart 4: Stock Status Distribution
        ax4 = fig.add_subplot(2, 2, 4)
        high = (stocks > 10).sum()
        medium = ((stocks > 5) & (stocks <= 10)).sum()
        low = (stocks <= 5).sum()
        
        categories = ['High Stock\n(>10)', 'Medium Stock\n(5-10)', 'Low Stock\n(≤5)']
        counts = np.array([high, medium, low])
        colors_status = ['#2ecc71', '#f39c12', '#e74c3c']
        
        bars = ax4.bar(categories, counts, color=colors_status, alpha=0.8, edgecolor='black', linewidth=1.5)
        ax4.set_ylabel('Number of Products', fontweight='bold', fontsize=10)
        ax4.set_title('Stock Status Distribution', fontweight='bold', fontsize=12, pad=15)
        ax4.grid(axis='y', alpha=0.3, linestyle='--')
        
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # Add statistics text
        total_value = values.sum()
        avg_stock = stocks.mean()
        stats_text = f'Total Inventory Value: ${total_value:.2f}\nAverage Stock: {avg_stock:.1f} units'
        fig.text(0.99, 0.01, stats_text, ha='right', va='bottom', fontsize=9, 
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        fig.tight_layout(pad=3.0)
        
        canvas = FigureCanvasTkAgg(fig, tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def create_sales_analytics(self, notebook):
        """Sales analytics with numpy, pandas, matplotlib"""
        tab = tk.Frame(notebook, bg='white')
        notebook.add(tab, text='📊 Sales Analytics')
        
        if not self.sales_history:
            tk.Label(tab, text="No sales data", font=('Arial', 14)).pack(expand=True)
            return
        
        fig = Figure(figsize=(14, 8), facecolor='white', dpi=100)
        
        # Create DataFrame using pandas
        df = pd.DataFrame(self.sales_history)
        df['date'] = pd.to_datetime(df['date'])
        df['date_only'] = df['date'].dt.date
        
        # Chart 1: Daily Revenue Trend
        ax1 = fig.add_subplot(2, 2, 1)
        daily_revenue = df.groupby('date_only')['total_amount'].sum()
        
        ax1.plot(range(len(daily_revenue)), daily_revenue.values, 
                marker='o', linewidth=2.5, markersize=7, color='#2ecc71', 
                markerfacecolor='#27ae60', markeredgecolor='white', markeredgewidth=2)
        ax1.fill_between(range(len(daily_revenue)), daily_revenue.values, 
                         alpha=0.3, color='#2ecc71')
        
        ax1.set_xlabel('Days', fontweight='bold', fontsize=10)
        ax1.set_ylabel('Revenue ($)', fontweight='bold', fontsize=10)
        ax1.set_title('Daily Sales Revenue Trend', fontweight='bold', fontsize=12, pad=15)
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.set_xticks(range(len(daily_revenue)))
        ax1.set_xticklabels([str(d) for d in daily_revenue.index], rotation=45, ha='right', fontsize=7)
        
        # Add trend line using numpy polyfit
        if len(daily_revenue) > 1:
            z = np.polyfit(range(len(daily_revenue)), daily_revenue.values, 1)
            p = np.poly1d(z)
            ax1.plot(range(len(daily_revenue)), p(range(len(daily_revenue))), 
                    "r--", alpha=0.8, linewidth=2, label=f'Trend: ${z[0]:.2f}/day')
            ax1.legend(fontsize=9)
        
        # Chart 2: Top Selling Products
        ax2 = fig.add_subplot(2, 2, 2)
        product_sales = df.groupby('product_name')['quantity'].sum().sort_values(ascending=True)
        top_10 = product_sales.tail(10)
        
        colors_grad = plt.cm.viridis(np.linspace(0.3, 0.9, len(top_10)))
        bars = ax2.barh(range(len(top_10)), top_10.values, color=colors_grad, 
                       alpha=0.8, edgecolor='black')
        ax2.set_yticks(range(len(top_10)))
        ax2.set_yticklabels([name[:20] for name in top_10.index], fontsize=9)
        ax2.set_xlabel('Quantity Sold', fontweight='bold', fontsize=10)
        ax2.set_title('Top 10 Best-Selling Products', fontweight='bold', fontsize=12, pad=15)
        ax2.grid(axis='x', alpha=0.3, linestyle='--')
        
        for i, (bar, value) in enumerate(zip(bars, top_10.values)):
            ax2.text(value + 0.5, i, f'{int(value)}', va='center', fontsize=9, fontweight='bold')
        
        # Chart 3: Revenue Distribution by Product
        ax3 = fig.add_subplot(2, 2, 3)
        product_revenue = df.groupby('product_name')['total_amount'].sum().sort_values(ascending=False)
        top_8 = product_revenue.head(8)
        
        explode = np.array([0.1 if i == 0 else 0.05 for i in range(len(top_8))])
        wedges, texts, autotexts = ax3.pie(top_8.values, labels=[n[:15] for n in top_8.index],
                                           autopct='%1.1f%%', startangle=90,
                                           colors=plt.cm.Set3.colors, explode=explode,
                                           shadow=True)
        for text in texts:
            text.set_fontsize(8)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(8)
        
        ax3.set_title('Revenue Distribution by Product', fontweight='bold', fontsize=12, pad=15)
        
        # Chart 4: Sales Volume Over Time
        ax4 = fig.add_subplot(2, 2, 4)
        daily_quantity = df.groupby('date_only')['quantity'].sum()
        
        colors_bars = plt.cm.coolwarm(np.linspace(0.2, 0.8, len(daily_quantity)))
        bars = ax4.bar(range(len(daily_quantity)), daily_quantity.values, 
                      color=colors_bars, alpha=0.8, edgecolor='black')
        
        ax4.set_xlabel('Days', fontweight='bold', fontsize=10)
        ax4.set_ylabel('Items Sold', fontweight='bold', fontsize=10)
        ax4.set_title('Daily Sales Volume (Units)', fontweight='bold', fontsize=12, pad=15)
        ax4.set_xticks(range(len(daily_quantity)))
        ax4.set_xticklabels([str(d) for d in daily_quantity.index], rotation=45, ha='right', fontsize=7)
        ax4.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Add average line
        avg_qty = daily_quantity.mean()
        ax4.axhline(y=avg_qty, color='r', linestyle='--', linewidth=2, 
                   label=f'Average: {avg_qty:.1f} units/day', alpha=0.7)
        ax4.legend(fontsize=9)
        
        # Add statistics
        total_sales = df['total_amount'].sum()
        total_items = df['quantity'].sum()
        stats_text = f'Total Revenue: ${total_sales:.2f}\nTotal Items Sold: {total_items}'
        fig.text(0.99, 0.01, stats_text, ha='right', va='bottom', fontsize=9,
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        
        fig.tight_layout(pad=3.0)
        
        canvas = FigureCanvasTkAgg(fig, tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def create_performance_analytics(self, notebook):
        """Product performance analytics"""
        tab = tk.Frame(notebook, bg='white')
        notebook.add(tab, text='🎯 Performance Metrics')
        
        if not self.products:
            tk.Label(tab, text="No performance data", font=('Arial', 14)).pack(expand=True)
            return
        
        fig = Figure(figsize=(14, 8), facecolor='white', dpi=100)
        
        # Prepare performance data
        perf_data = pd.DataFrame([
            {
                'name': p['name'],
                'stock': p['quantity'],
                'sold': p['total_sold'],
                'price': p['price'],
                'revenue': p['price'] * p['total_sold'],
                'turnover': p['total_sold'] / (p['total_sold'] + p['quantity']) * 100 if (p['total_sold'] + p['quantity']) > 0 else 0
            }
            for p in self.products.values()
        ])
        
        # Chart 1: Product Performance Matrix (Scatter Plot)
        ax1 = fig.add_subplot(2, 2, 1)
        scatter = ax1.scatter(perf_data['sold'], perf_data['revenue'], 
                            s=perf_data['price']*20, alpha=0.6, 
                            c=perf_data['turnover'], cmap='RdYlGn',
                            edgecolors='black', linewidth=1.5)
        
        ax1.set_xlabel('Units Sold', fontweight='bold', fontsize=10)
        ax1.set_ylabel('Revenue Generated ($)', fontweight='bold', fontsize=10)
        ax1.set_title('Product Performance Matrix', fontweight='bold', fontsize=12, pad=15)
        ax1.grid(True, alpha=0.3, linestyle='--')
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax1)
        cbar.set_label('Turnover Rate (%)', fontweight='bold', fontsize=9)
        
        # Annotate top performers
        for idx, row in perf_data.nlargest(3, 'revenue').iterrows():
            ax1.annotate(row['name'][:10], (row['sold'], row['revenue']),
                        xytext=(5, 5), textcoords='offset points', fontsize=7,
                        bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
        
        # Chart 2: Revenue per Product (Horizontal Bar)
        ax2 = fig.add_subplot(2, 2, 2)
        top_revenue = perf_data.nlargest(10, 'revenue').sort_values('revenue')
        
        colors = plt.cm.plasma(np.linspace(0.3, 0.9, len(top_revenue)))
        bars = ax2.barh(range(len(top_revenue)), top_revenue['revenue'], 
                       color=colors, alpha=0.8, edgecolor='black')
        ax2.set_yticks(range(len(top_revenue)))
        ax2.set_yticklabels([n[:20] for n in top_revenue['name']], fontsize=9)
        ax2.set_xlabel('Revenue ($)', fontweight='bold', fontsize=10)
        ax2.set_title('Top 10 Revenue Generators', fontweight='bold', fontsize=12, pad=15)
        ax2.grid(axis='x', alpha=0.3, linestyle='--')
        
        for i, (bar, value) in enumerate(zip(bars, top_revenue['revenue'])):
            ax2.text(value + max(top_revenue['revenue'])*0.01, i, f'${value:.0f}',
                    va='center', fontsize=8, fontweight='bold')
        
        # Chart 3: Turnover Rate Analysis
        ax3 = fig.add_subplot(2, 2, 3)
        sorted_turnover = perf_data.sort_values('turnover', ascending=False)
        
        colors_turn = ['#2ecc71' if x > 50 else '#f39c12' if x > 25 else '#e74c3c' 
                      for x in sorted_turnover['turnover']]
        
        bars = ax3.bar(range(len(sorted_turnover)), sorted_turnover['turnover'],
                      color=colors_turn, alpha=0.8, edgecolor='black')
        ax3.set_xlabel('Products', fontweight='bold', fontsize=10)
        ax3.set_ylabel('Turnover Rate (%)', fontweight='bold', fontsize=10)
        ax3.set_title('Product Turnover Rate', fontweight='bold', fontsize=12, pad=15)
        ax3.set_xticks(range(len(sorted_turnover)))
        ax3.set_xticklabels([n[:12] for n in sorted_turnover['name']], 
                           rotation=45, ha='right', fontsize=7)
        ax3.grid(axis='y', alpha=0.3, linestyle='--')
        ax3.axhline(y=50, color='green', linestyle='--', alpha=0.5, label='Good (>50%)')
        ax3.axhline(y=25, color='orange', linestyle='--', alpha=0.5, label='Fair (>25%)')
        ax3.legend(fontsize=8, loc='upper right')
        
        # Chart 4: Price vs Sales Correlation
        ax4 = fig.add_subplot(2, 2, 4)
        
        # Create price bins
        price_bins = pd.cut(perf_data['price'], bins=5)
        price_sales = perf_data.groupby(price_bins)['sold'].sum()
        
        bin_labels = [f'${interval.left:.0f}-${interval.right:.0f}' 
                     for interval in price_sales.index]
        
        bars = ax4.bar(range(len(price_sales)), price_sales.values,
                      color='#9b59b6', alpha=0.8, edgecolor='black')
        ax4.set_xlabel('Price Range', fontweight='bold', fontsize=10)
        ax4.set_ylabel('Units Sold', fontweight='bold', fontsize=10)
        ax4.set_title('Sales by Price Range', fontweight='bold', fontsize=12, pad=15)
        ax4.set_xticks(range(len(price_sales)))
        ax4.set_xticklabels(bin_labels, rotation=45, ha='right', fontsize=8)
        ax4.grid(axis='y', alpha=0.3, linestyle='--')
        
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom', 
                    fontsize=9, fontweight='bold')
        
        # Add statistics
        avg_turnover = perf_data['turnover'].mean()
        best_product = perf_data.loc[perf_data['revenue'].idxmax(), 'name']
        stats_text = f'Avg Turnover: {avg_turnover:.1f}%\nBest Product: {best_product[:15]}'
        fig.text(0.99, 0.01, stats_text, ha='right', va='bottom', fontsize=9,
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
        
        fig.tight_layout(pad=3.0)
        
        canvas = FigureCanvasTkAgg(fig, tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def create_financial_analytics(self, notebook):
        """Financial analytics dashboard"""
        tab = tk.Frame(notebook, bg='white')
        notebook.add(tab, text='💰 Financial Summary')
        
        fig = Figure(figsize=(14, 8), facecolor='white', dpi=100)
        
        # Prepare financial data
        if self.products:
            product_df = pd.DataFrame([
                {
                    'name': p['name'],
                    'revenue': p['price'] * p['total_sold'],
                    'inventory_value': p['price'] * p['quantity'],
                    'profit_margin': 30  # Assumed 30% profit margin
                }
                for p in self.products.values()
            ])
        else:
            product_df = pd.DataFrame()
        
        # Chart 1: Revenue vs Inventory Value
        ax1 = fig.add_subplot(2, 2, 1)
        if not product_df.empty:
            x = np.arange(len(product_df))
            width = 0.35
            
            bars1 = ax1.bar(x - width/2, product_df['revenue'], width,
                          label='Revenue', color='#2ecc71', alpha=0.8, edgecolor='black')
            bars2 = ax1.bar(x + width/2, product_df['inventory_value'], width,
                          label='Inventory Value', color='#3498db', alpha=0.8, edgecolor='black')
            
            ax1.set_xlabel('Products', fontweight='bold', fontsize=10)
            ax1.set_ylabel('Amount ($)', fontweight='bold', fontsize=10)
            ax1.set_title('Revenue vs Inventory Value', fontweight='bold', fontsize=12, pad=15)
            ax1.set_xticks(x)
            ax1.set_xticklabels([n[:12] for n in product_df['name']], 
                               rotation=45, ha='right', fontsize=8)
            ax1.legend(fontsize=9)
            ax1.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Chart 2: Revenue Breakdown
        ax2 = fig.add_subplot(2, 2, 2)
        total_revenue = self.total_revenue
        total_inventory = sum(p['price'] * p['quantity'] for p in self.products.values())
        estimated_profit = total_revenue * 0.30
        
        financial_data = np.array([total_revenue, total_inventory, estimated_profit])
        labels = ['Total Revenue', 'Inventory Value', 'Est. Profit (30%)']
        colors_fin = ['#2ecc71', '#3498db', '#f39c12']
        
        bars = ax2.bar(range(3), financial_data, color=colors_fin, 
                      alpha=0.8, edgecolor='black', linewidth=2)
        ax2.set_ylabel('Amount ($)', fontweight='bold', fontsize=10)
        ax2.set_title('Financial Overview', fontweight='bold', fontsize=12, pad=15)
        ax2.set_xticks(range(3))
        ax2.set_xticklabels(labels, fontsize=9)
        ax2.grid(axis='y', alpha=0.3, linestyle='--')
        
        for bar, value in zip(bars, financial_data):
            ax2.text(bar.get_x() + bar.get_width()/2., value,
                    f'${value:.2f}', ha='center', va='bottom',
                    fontsize=10, fontweight='bold')
        
        # Chart 3: Sales Trend with Moving Average
        ax3 = fig.add_subplot(2, 2, 3)
        if self.sales_history:
            df = pd.DataFrame(self.sales_history)
            df['date'] = pd.to_datetime(df['date'])
            df['date_only'] = df['date'].dt.date
            daily_rev = df.groupby('date_only')['total_amount'].sum()
            
            # Plot daily revenue
            ax3.plot(range(len(daily_rev)), daily_rev.values,
                    marker='o', linewidth=2, markersize=6, color='#3498db',
                    label='Daily Revenue', alpha=0.7)
            
            # Calculate moving average if enough data
            if len(daily_rev) >= 3:
                window = min(3, len(daily_rev))
                moving_avg = pd.Series(daily_rev.values).rolling(window=window).mean()
                ax3.plot(range(len(moving_avg)), moving_avg.values,
                        linewidth=3, color='#e74c3c', linestyle='--',
                        label=f'{window}-Day Moving Avg', alpha=0.8)
            
            ax3.set_xlabel('Days', fontweight='bold', fontsize=10)
            ax3.set_ylabel('Revenue ($)', fontweight='bold', fontsize=10)
            ax3.set_title('Revenue Trend Analysis', fontweight='bold', fontsize=12, pad=15)
            ax3.legend(fontsize=9)
            ax3.grid(True, alpha=0.3, linestyle='--')
            ax3.fill_between(range(len(daily_rev)), daily_rev.values, alpha=0.2, color='#3498db')
        
        # Chart 4: Key Performance Indicators
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.axis('off')
        
        # Calculate KPIs
        total_products = len(self.products)
        total_sales_count = len(self.sales_history)
        avg_order_value = total_revenue / total_sales_count if total_sales_count > 0 else 0
        total_items_sold = sum(p['total_sold'] for p in self.products.values())
        
        # Create KPI display
        kpi_text = f"""
        KEY PERFORMANCE INDICATORS (KPIs)
        {'='*50}
        
        📊 Sales Metrics:
           • Total Revenue: ${total_revenue:,.2f}
           • Total Transactions: {total_sales_count}
           • Average Order Value: ${avg_order_value:.2f}
           • Total Units Sold: {total_items_sold}
        
        📦 Inventory Metrics:
           • Total Products: {total_products}
           • Inventory Value: ${total_inventory:,.2f}
           • Avg Product Value: ${total_inventory/total_products if total_products > 0 else 0:.2f}
        
        💰 Financial Metrics:
           • Estimated Profit: ${estimated_profit:,.2f}
           • Profit Margin: 30.0%
           • ROI: {(total_revenue/total_inventory*100 if total_inventory > 0 else 0):.1f}%
        
        🎯 Performance:
           • Stock Turnover: {(total_items_sold/(total_items_sold + sum(p['quantity'] for p in self.products.values()))*100 if (total_items_sold + sum(p['quantity'] for p in self.products.values())) > 0 else 0):.1f}%
        """
        
        ax4.text(0.5, 0.5, kpi_text, ha='center', va='center',
                fontsize=10, family='monospace',
                bbox=dict(boxstyle='round,pad=1', facecolor='#ecf0f1', 
                         edgecolor='#34495e', linewidth=2))
        
        ax4.set_title('Business KPI Dashboard', fontweight='bold', 
                     fontsize=14, pad=20, loc='center')
        
        fig.tight_layout(pad=3.0)
        
        canvas = FigureCanvasTkAgg(fig, tab)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def on_closing(self):
        """Handle window closing"""
        if messagebox.askokcancel("Quit", "Save data before quitting?"):
            self.save_data()
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

def main():
    print("="*60)
    print("🚀 E-COMMERCE STORE MANAGEMENT SYSTEM")
    print("   Complete with Data Visualization")
    print("   For BBA Students")
    print("="*60)
    print("\n📊 Features:")
    print("   ✓ Inventory Management")
    print("   ✓ Sales Processing")
    print("   ✓ Business Analytics")
    print("   ✓ Data Visualization (Numpy, Pandas, Matplotlib)")
    print("   ✓ Performance Metrics")
    print("   ✓ Financial Reports")
    print("\n💡 Quick Start Guide:")
    print("   1. Add products using 'Add Product' button")
    print("   2. Process orders using 'Process Order' button")
    print("   3. View analytics using 'Analytics' button")
    print("   4. Generate reports and visualizations")
    print("\n" + "="*60)
    
    app = EcommerceStoreComplete()
    app.run()

if __name__ == "__main__":
    main()