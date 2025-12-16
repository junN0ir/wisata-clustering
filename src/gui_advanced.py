import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd

class WisataClusteringAdvancedGUI:
    """
    GUI Advanced untuk clustering wisata dengan fitur:
    - Cluster overview
    - Statistics
    - Filter by cluster/kategori
    - Export functionality
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Clustering Wisata Balikpapan - Advanced")
        self.root.geometry("1400x800")
        
        # Color scheme - Modern & Clean
        self.colors = {
            'bg': '#f5f7fa',
            'primary': '#1e3a8a',
            'secondary': '#3b82f6',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'info': '#06b6d4',
            'light': '#e0e7ff',
            'white': '#ffffff',
            'text': '#1f2937',
            'text_light': '#6b7280'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        # Filter state
        self.current_filter = {'cluster': 'all', 'kategori': 'all'}
        
        # Load data
        self.load_data()
        
        # Setup UI
        self.setup_ui()
        
    def load_data(self):
        """Load data dari CSV"""
        try:
            self.df_hasil = pd.read_csv("../outputs/hasil_cluster_per_tempat.csv")
            self.df_raw = pd.read_csv("../data/raw/wisata_balikpapan.csv")
            
            try:
                self.df_cluster = pd.read_csv("../outputs/detail_cluster.csv")
            except:
                self.df_cluster = None
                
        except Exception as e:
            messagebox.showerror("Error", 
                f"Gagal load data: {str(e)}\n\n"
                "Pastikan sudah menjalankan main.py terlebih dahulu!"
            )
            self.root.quit()
    
    def setup_ui(self):
        """Setup UI components"""
        
        # ========== TOP BAR ==========
        self.create_top_bar()
        
        # ========== TOOLBAR ==========
        self.create_toolbar()
        
        # ========== MAIN CONTENT ==========
        content = tk.Frame(self.root, bg=self.colors['bg'])
        content.pack(fill='both', expand=True, padx=10, pady=5)
        
        # LEFT: Sidebar with filters and list
        self.create_sidebar(content)
        
        # RIGHT: Detail panel
        self.create_detail_panel(content)
        
        # ========== STATUS BAR ==========
        self.create_status_bar()
    
    def create_top_bar(self):
        """Create top bar with title and stats"""
        top_bar = tk.Frame(self.root, bg=self.colors['primary'], height=100)
        top_bar.pack(fill='x', side='top')
        top_bar.pack_propagate(False)
        
        # Title
        title = tk.Label(
            top_bar,
            text="🏝️ Clustering Wisata Balikpapan",
            font=('Segoe UI', 28, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        title.pack(side='left', padx=30, pady=25)
        
        # Quick stats
        stats_frame = tk.Frame(top_bar, bg=self.colors['primary'])
        stats_frame.pack(side='right', padx=30)
        
        stats = [
            ("📍 Tempat", len(self.df_hasil)),
            ("🏷️ Cluster", self.df_hasil['cluster'].nunique()),
            ("💬 Review", len(self.df_raw))
        ]
        
        for label, value in stats:
            stat_box = tk.Frame(stats_frame, bg=self.colors['secondary'], 
                              relief='flat', bd=0)
            stat_box.pack(side='left', padx=5)
            
            tk.Label(
                stat_box,
                text=str(value),
                font=('Segoe UI', 20, 'bold'),
                bg=self.colors['secondary'],
                fg=self.colors['white']
            ).pack(padx=15, pady=(10, 0))
            
            tk.Label(
                stat_box,
                text=label,
                font=('Segoe UI', 10),
                bg=self.colors['secondary'],
                fg=self.colors['white']
            ).pack(padx=15, pady=(0, 10))
    
    def create_toolbar(self):
        """Create toolbar with filters"""
        toolbar = tk.Frame(self.root, bg=self.colors['white'], 
                          relief='solid', bd=1, height=50)
        toolbar.pack(fill='x', padx=10, pady=(5, 0))
        toolbar.pack_propagate(False)
        
        # Filter label
        tk.Label(
            toolbar,
            text="🔍 Filter:",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['white']
        ).pack(side='left', padx=(15, 10))
        
        # Cluster filter
        tk.Label(
            toolbar,
            text="Cluster:",
            font=('Segoe UI', 10),
            bg=self.colors['white']
        ).pack(side='left', padx=(0, 5))
        
        self.cluster_filter = ttk.Combobox(
            toolbar,
            values=['Semua'] + [f"Cluster {i}" for i in sorted(self.df_hasil['cluster'].unique())],
            state='readonly',
            width=12,
            font=('Segoe UI', 10)
        )
        self.cluster_filter.set('Semua')
        self.cluster_filter.pack(side='left', padx=(0, 20))
        self.cluster_filter.bind('<<ComboboxSelected>>', self.apply_filters)
        
        # Kategori filter
        tk.Label(
            toolbar,
            text="Kategori:",
            font=('Segoe UI', 10),
            bg=self.colors['white']
        ).pack(side='left', padx=(0, 5))
        
        self.kategori_filter = ttk.Combobox(
            toolbar,
            values=['Semua'] + sorted(self.df_hasil['kategori'].unique().tolist()),
            state='readonly',
            width=15,
            font=('Segoe UI', 10)
        )
        self.kategori_filter.set('Semua')
        self.kategori_filter.pack(side='left', padx=(0, 20))
        self.kategori_filter.bind('<<ComboboxSelected>>', self.apply_filters)
        
        # Reset button
        reset_btn = tk.Button(
            toolbar,
            text="↻ Reset",
            font=('Segoe UI', 10),
            bg=self.colors['info'],
            fg=self.colors['white'],
            relief='flat',
            padx=15,
            cursor='hand2',
            command=self.reset_filters
        )
        reset_btn.pack(side='left', padx=5)
    
    def create_sidebar(self, parent):
        """Create sidebar with list"""
        sidebar = tk.Frame(parent, bg=self.colors['white'], 
                          relief='solid', bd=1, width=350)
        sidebar.pack(side='left', fill='both', padx=(0, 5))
        sidebar.pack_propagate(False)
        
        # Header
        header = tk.Label(
            sidebar,
            text="📋 Daftar Tempat Wisata",
            font=('Segoe UI', 13, 'bold'),
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            pady=12
        )
        header.pack(fill='x')
        
        # Search
        search_frame = tk.Frame(sidebar, bg=self.colors['white'])
        search_frame.pack(fill='x', padx=15, pady=10)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_list)
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 11),
            relief='solid',
            bd=1
        )
        search_entry.pack(fill='x')
        
        search_placeholder = tk.Label(
            search_frame,
            text="💡 Ketik untuk mencari...",
            font=('Segoe UI', 9),
            fg=self.colors['text_light'],
            bg=self.colors['white'],
            anchor='w'
        )
        search_placeholder.pack(fill='x', pady=(2, 0))
        
        # Listbox with custom styling
        list_container = tk.Frame(sidebar, bg=self.colors['white'])
        list_container.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side='right', fill='y')
        
        self.wisata_listbox = tk.Listbox(
            list_container,
            font=('Segoe UI', 11),
            yscrollcommand=scrollbar.set,
            relief='flat',
            bd=0,
            selectmode='single',
            activestyle='none',
            selectbackground=self.colors['secondary'],
            selectforeground=self.colors['white'],
            highlightthickness=0,
            bg=self.colors['white']
        )
        self.wisata_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.wisata_listbox.yview)
        
        self.populate_listbox()
        self.wisata_listbox.bind('<<ListboxSelect>>', self.on_select_wisata)
        
        # Count label
        self.count_label = tk.Label(
            sidebar,
            text=f"Menampilkan: {len(self.df_hasil)} tempat",
            font=('Segoe UI', 9),
            bg=self.colors['light'],
            fg=self.colors['text'],
            pady=8
        )
        self.count_label.pack(fill='x', side='bottom')
    
    def create_detail_panel(self, parent):
        """Create detail panel"""
        detail_container = tk.Frame(parent, bg=self.colors['white'], 
                                   relief='solid', bd=1)
        detail_container.pack(side='right', fill='both', expand=True)
        
        # Header
        self.detail_header = tk.Label(
            detail_container,
            text="ℹ️ Detail Tempat Wisata",
            font=('Segoe UI', 13, 'bold'),
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            pady=12
        )
        self.detail_header.pack(fill='x')
        
        # Scrollable content
        canvas = tk.Canvas(detail_container, bg=self.colors['white'], 
                          highlightthickness=0)
        scrollbar = tk.Scrollbar(detail_container, orient="vertical", 
                                command=canvas.yview)
        self.detail_frame = tk.Frame(canvas, bg=self.colors['white'])
        
        self.detail_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.detail_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel binding
        canvas.bind_all("<MouseWheel>", 
                       lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        self.show_welcome()
    
    def create_status_bar(self):
        """Create status bar"""
        status = tk.Frame(self.root, bg=self.colors['primary'], height=30)
        status.pack(fill='x', side='bottom')
        status.pack_propagate(False)
        
        self.status_label = tk.Label(
            status,
            text="✅ Siap | Implementasi Custom: TF-IDF + K-Means",
            font=('Segoe UI', 9),
            bg=self.colors['primary'],
            fg=self.colors['white'],
            anchor='w'
        )
        self.status_label.pack(side='left', padx=15, fill='x', expand=True)
    
    def populate_listbox(self, filtered_df=None):
        """Populate listbox"""
        self.wisata_listbox.delete(0, tk.END)
        
        df = filtered_df if filtered_df is not None else self.df_hasil
        
        for idx, row in df.sort_values('cluster').iterrows():
            emoji = self.get_kategori_emoji(row['kategori'])
            display = f"{emoji} [C{row['cluster']}] {row['wisata']}"
            self.wisata_listbox.insert(tk.END, display)
        
        self.count_label.config(text=f"Menampilkan: {len(df)} tempat")
    
    def filter_list(self, *args):
        """Filter list based on search"""
        search = self.search_var.get().lower()
        filtered = self.df_hasil[
            self.df_hasil['wisata'].str.lower().str.contains(search)
        ]
        
        # Apply existing filters
        if self.current_filter['cluster'] != 'all':
            filtered = filtered[filtered['cluster'] == self.current_filter['cluster']]
        if self.current_filter['kategori'] != 'all':
            filtered = filtered[filtered['kategori'] == self.current_filter['kategori']]
        
        self.populate_listbox(filtered)
    
    def apply_filters(self, event=None):
        """Apply cluster and kategori filters"""
        cluster_val = self.cluster_filter.get()
        kategori_val = self.kategori_filter.get()
        
        # Update filter state
        if cluster_val == 'Semua':
            self.current_filter['cluster'] = 'all'
        else:
            self.current_filter['cluster'] = int(cluster_val.split()[-1])
        
        if kategori_val == 'Semua':
            self.current_filter['kategori'] = 'all'
        else:
            self.current_filter['kategori'] = kategori_val
        
        # Apply filters
        filtered = self.df_hasil.copy()
        
        if self.current_filter['cluster'] != 'all':
            filtered = filtered[filtered['cluster'] == self.current_filter['cluster']]
        
        if self.current_filter['kategori'] != 'all':
            filtered = filtered[filtered['kategori'] == self.current_filter['kategori']]
        
        # Apply search if any
        search = self.search_var.get().lower()
        if search:
            filtered = filtered[filtered['wisata'].str.lower().str.contains(search)]
        
        self.populate_listbox(filtered)
        self.status_label.config(text=f"✅ Filter diterapkan: {len(filtered)} hasil")
    
    def reset_filters(self):
        """Reset all filters"""
        self.cluster_filter.set('Semua')
        self.kategori_filter.set('Semua')
        self.search_var.set('')
        self.current_filter = {'cluster': 'all', 'kategori': 'all'}
        self.populate_listbox()
        self.status_label.config(text="✅ Filter direset")
    
    def show_welcome(self):
        """Show welcome message"""
        for widget in self.detail_frame.winfo_children():
            widget.destroy()
        
        welcome = tk.Frame(self.detail_frame, bg=self.colors['white'])
        welcome.pack(fill='both', expand=True, pady=100)
        
        tk.Label(
            welcome,
            text="👈",
            font=('Segoe UI', 60),
            bg=self.colors['white']
        ).pack()
        
        tk.Label(
            welcome,
            text="Pilih tempat wisata",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['text']
        ).pack(pady=10)
        
        tk.Label(
            welcome,
            text="untuk melihat detail analisis",
            font=('Segoe UI', 12),
            bg=self.colors['white'],
            fg=self.colors['text_light']
        ).pack()
    
    def on_select_wisata(self, event):
        """Handle selection"""
        selection = self.wisata_listbox.curselection()
        if not selection:
            return
        
        selected = self.wisata_listbox.get(selection[0])
        # Extract name
        parts = selected.split('] ', 1)
        if len(parts) > 1:
            name = parts[1]
        else:
            name = selected
        
        self.show_detail(name)
        self.status_label.config(text=f"✅ Menampilkan: {name}")
    
    def show_detail(self, wisata_name):
        """Show detail for selected wisata"""
        for widget in self.detail_frame.winfo_children():
            widget.destroy()
        
        # Get data
        data = self.df_hasil[self.df_hasil['wisata'] == wisata_name].iloc[0]
        reviews = self.df_raw[self.df_raw['wisata'] == wisata_name]['review'].tolist()
        
        # Update header
        self.detail_header.config(text=f"📍 {wisata_name}")
        
        # Main container
        main = tk.Frame(self.detail_frame, bg=self.colors['white'])
        main.pack(fill='both', expand=True, padx=25, pady=20)
        
        # Info cards
        self.create_info_cards(main, data)
        
        # Reviews section
        self.create_reviews_section(main, reviews)
    
    def create_info_cards(self, parent, data):
        """Create info cards"""
        cards_container = tk.Frame(parent, bg=self.colors['white'])
        cards_container.pack(fill='x', pady=(0, 20))
        
        # Cluster card
        self.create_card(
            cards_container,
            "🏷️ Cluster",
            f"Cluster {data['cluster']}",
            data['cluster_label'],
            self.colors['primary']
        ).pack(fill='x', pady=5)
        
        # Kategori card
        self.create_card(
            cards_container,
            "⭐ Kategori",
            data['kategori'],
            self.get_kategori_desc(data['kategori']),
            self.get_kategori_color(data['kategori'])
        ).pack(fill='x', pady=5)
        
        # Tema card
        self.create_card(
            cards_container,
            "🎯 Tema",
            data['tema_utama'],
            f"Kategori: {data['tema_utama']}",
            self.colors['info']
        ).pack(fill='x', pady=5)
        
        # Keywords card
        keywords_card = tk.Frame(cards_container, bg=self.colors['light'], 
                                relief='solid', bd=1)
        keywords_card.pack(fill='x', pady=5)
        
        tk.Label(
            keywords_card,
            text="🔑 Kata Kunci",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['light'],
            fg=self.colors['text'],
            anchor='w'
        ).pack(fill='x', padx=15, pady=(10, 5))
        
        # Keywords as tags
        tags_frame = tk.Frame(keywords_card, bg=self.colors['light'])
        tags_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        keywords = data['kata_kunci'].split(', ')
        for kw in keywords:
            tag = tk.Label(
                tags_frame,
                text=kw,
                font=('Segoe UI', 10),
                bg=self.colors['secondary'],
                fg=self.colors['white'],
                padx=10,
                pady=5,
                relief='flat'
            )
            tag.pack(side='left', padx=3, pady=2)
    
    def create_card(self, parent, title, value, subtitle, color):
        """Create info card"""
        card = tk.Frame(parent, bg=self.colors['light'], relief='solid', bd=1)
        
        header = tk.Frame(card, bg=color)
        header.pack(fill='x')
        
        tk.Label(
            header,
            text=title,
            font=('Segoe UI', 11, 'bold'),
            bg=color,
            fg=self.colors['white'],
            anchor='w'
        ).pack(fill='x', padx=15, pady=8)
        
        body = tk.Frame(card, bg=self.colors['light'])
        body.pack(fill='x', padx=15, pady=10)
        
        tk.Label(
            body,
            text=value,
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['light'],
            fg=self.colors['text'],
            anchor='w'
        ).pack(fill='x')
        
        tk.Label(
            body,
            text=subtitle,
            font=('Segoe UI', 10),
            bg=self.colors['light'],
            fg=self.colors['text_light'],
            anchor='w'
        ).pack(fill='x', pady=(2, 0))
        
        return card
    
    def create_reviews_section(self, parent, reviews):
        """Create reviews section"""
        section = tk.Frame(parent, bg=self.colors['white'])
        section.pack(fill='both', expand=True)
        
        # Header
        header = tk.Frame(section, bg=self.colors['secondary'])
        header.pack(fill='x')
        
        tk.Label(
            header,
            text=f"💬 Review Pengunjung ({len(reviews)} review)",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            anchor='w'
        ).pack(fill='x', padx=15, pady=10)
        
        # Reviews
        for i, review in enumerate(reviews, 1):
            review_card = tk.Frame(section, bg=self.colors['light'], 
                                  relief='solid', bd=1)
            review_card.pack(fill='x', pady=8)
            
            # Number badge
            badge = tk.Label(
                review_card,
                text=f"#{i}",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['info'],
                fg=self.colors['white'],
                padx=10,
                pady=5
            )
            badge.pack(anchor='nw', padx=10, pady=10)
            
            # Review text
            tk.Label(
                review_card,
                text=review,
                font=('Segoe UI', 11),
                bg=self.colors['light'],
                fg=self.colors['text'],
                wraplength=700,
                justify='left',
                anchor='w'
            ).pack(fill='x', padx=15, pady=(0, 15))
    
    def get_kategori_emoji(self, kategori):
        """Get emoji for kategori"""
        emojis = {
            'Sangat Baik': '⭐',
            'Baik': '👍',
            'Kurang Baik': '👎',
            'Netral': '➖'
        }
        return emojis.get(kategori, '📍')
    
    def get_kategori_color(self, kategori):
        """Get color for kategori"""
        colors = {
            'Sangat Baik': self.colors['success'],
            'Baik': self.colors['secondary'],
            'Kurang Baik': self.colors['danger'],
            'Netral': self.colors['warning']
        }
        return colors.get(kategori, self.colors['primary'])
    
    def get_kategori_desc(self, kategori):
        """Get description for kategori"""
        descs = {
            'Sangat Baik': 'Tempat wisata dengan review sangat positif',
            'Baik': 'Tempat wisata dengan review positif',
            'Kurang Baik': 'Tempat wisata dengan review negatif',
            'Netral': 'Tempat wisata dengan review beragam'
        }
        return descs.get(kategori, 'Tidak ada deskripsi')


def main():
    root = tk.Tk()
    app = WisataClusteringAdvancedGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()