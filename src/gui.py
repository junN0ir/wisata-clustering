import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from pathlib import Path

class WisataClusteringGUI:
    """
    GUI Lengkap untuk menampilkan hasil clustering wisata Balikpapan
    Dengan fitur filtering dan statistik
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Clustering Wisata Balikpapan - Hasil Analisis")
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
            # Load hasil clustering
            self.df_hasil = pd.read_csv("../outputs/hasil_cluster_per_tempat.csv")
            
            # Load data asli untuk review
            self.df_raw = pd.read_csv("../data/raw/wisata_balikpapan.csv")
            
            # Load detail cluster
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
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=10, pady=5)
        
        # LEFT PANEL: Daftar tempat
        self.create_left_panel(main_container)
        
        # RIGHT PANEL: Detail tempat
        self.create_right_panel(main_container)
        
        # ========== STATUS BAR ==========
        self.create_status_bar()
    
    def create_top_bar(self):
        """Create top bar with title and statistics"""
        top_bar = tk.Frame(self.root, bg=self.colors['primary'], height=100)
        top_bar.pack(fill='x', side='top')
        top_bar.pack_propagate(False)
        
        # Title
        title_label = tk.Label(
            top_bar,
            text="🏝️ Clustering Wisata Balikpapan",
            font=('Segoe UI', 26, 'bold'),
            bg=self.colors['primary'],
            fg=self.colors['white']
        )
        title_label.pack(side='left', padx=30, pady=25)
        
        # Quick statistics
        stats_frame = tk.Frame(top_bar, bg=self.colors['primary'])
        stats_frame.pack(side='right', padx=30)
        
        stats_data = [
            ("📍 Tempat", len(self.df_hasil)),
            ("🏷️ Cluster", self.df_hasil['cluster'].nunique()),
            ("💬 Review", len(self.df_raw))
        ]
        
        for label, value in stats_data:
            stat_box = tk.Frame(stats_frame, bg=self.colors['secondary'], relief='flat')
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
        toolbar = tk.Frame(self.root, bg=self.colors['white'], relief='solid', bd=1, height=50)
        toolbar.pack(fill='x', padx=10, pady=(5, 0))
        toolbar.pack_propagate(False)
        
        # Filter icon and label
        tk.Label(
            toolbar,
            text="🔍 Filter:",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['text']
        ).pack(side='left', padx=(15, 10))
        
        # Cluster filter
        tk.Label(
            toolbar,
            text="Cluster:",
            font=('Segoe UI', 10),
            bg=self.colors['white'],
            fg=self.colors['text']
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
            bg=self.colors['white'],
            fg=self.colors['text']
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
            text="↻ Reset Filter",
            font=('Segoe UI', 10),
            bg=self.colors['info'],
            fg=self.colors['white'],
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            activebackground=self.colors['secondary'],
            command=self.reset_filters
        )
        reset_btn.pack(side='left', padx=5)
        
        # Separator
        separator = tk.Frame(toolbar, bg=self.colors['text_light'], width=2)
        separator.pack(side='left', fill='y', padx=15, pady=8)
        
        # Info label
        tk.Label(
            toolbar,
            text="💡 Tip: Klik tempat untuk melihat detail",
            font=('Segoe UI', 9, 'italic'),
            bg=self.colors['white'],
            fg=self.colors['text_light']
        ).pack(side='left', padx=5)
    
    def create_left_panel(self, parent):
        """Create left panel with list"""
        left_panel = tk.Frame(parent, bg=self.colors['white'], relief='solid', bd=1, width=380)
        left_panel.pack(side='left', fill='both', padx=(0, 5))
        left_panel.pack_propagate(False)
        
        # Header
        header = tk.Label(
            left_panel,
            text="📋 Daftar Tempat Wisata",
            font=('Segoe UI', 13, 'bold'),
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            pady=12
        )
        header.pack(fill='x')
        
        # Search frame
        search_frame = tk.Frame(left_panel, bg=self.colors['white'])
        search_frame.pack(fill='x', padx=15, pady=12)
        
        # Search label
        tk.Label(
            search_frame,
            text="🔎",
            font=('Segoe UI', 12),
            bg=self.colors['white']
        ).pack(side='left', padx=(0, 5))
        
        # Search entry
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_list)
        
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 11),
            relief='solid',
            bd=1
        )
        search_entry.pack(side='left', fill='x', expand=True)
        
        # Search hint
        tk.Label(
            left_panel,
            text="💡 Ketik nama tempat untuk mencari...",
            font=('Segoe UI', 9, 'italic'),
            bg=self.colors['light'],
            fg=self.colors['text_light'],
            pady=5
        ).pack(fill='x', padx=15)
        
        # Listbox container
        list_container = tk.Frame(left_panel, bg=self.colors['white'])
        list_container.pack(fill='both', expand=True, padx=10, pady=(10, 10))
        
        # Scrollbar
        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side='right', fill='y')
        
        # Listbox
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
        
        # Bind selection event
        self.wisata_listbox.bind('<<ListboxSelect>>', self.on_select_wisata)
        
        # Count label - BUAT DULU sebelum populate
        self.count_label = tk.Label(
            left_panel,
            text=f"Menampilkan: {len(self.df_hasil)} tempat",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['light'],
            fg=self.colors['text'],
            pady=10
        )
        self.count_label.pack(fill='x', side='bottom')
        
        # Populate listbox - SETELAH count_label dibuat
        self.populate_listbox()
    
    def create_right_panel(self, parent):
        """Create right panel for details"""
        right_panel = tk.Frame(parent, bg=self.colors['white'], relief='solid', bd=1)
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Header
        self.detail_title = tk.Label(
            right_panel,
            text="ℹ️ Detail Tempat Wisata",
            font=('Segoe UI', 13, 'bold'),
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            pady=12
        )
        self.detail_title.pack(fill='x')
        
        # Scrollable canvas
        canvas = tk.Canvas(right_panel, bg=self.colors['white'], highlightthickness=0)
        scrollbar_right = tk.Scrollbar(right_panel, orient="vertical", command=canvas.yview)
        
        # CREATE scrollable_frame DULU sebelum show_welcome_message
        self.scrollable_frame = tk.Frame(canvas, bg=self.colors['white'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_right.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_right.pack(side="right", fill="y")
        
        # Bind mouse wheel
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
        # Show welcome message - SETELAH scrollable_frame dibuat
        self.show_welcome_message()
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        status_bar = tk.Frame(self.root, bg=self.colors['primary'], height=30)
        status_bar.pack(fill='x', side='bottom')
        status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_bar,
            text="✅ Siap | Implementasi Custom: TF-IDF + K-Means (No Sklearn)",
            font=('Segoe UI', 9),
            bg=self.colors['primary'],
            fg=self.colors['white'],
            anchor='w'
        )
        self.status_label.pack(side='left', padx=15, fill='x', expand=True)
    
    def populate_listbox(self, filtered_df=None):
        """Populate listbox with wisata data"""
        self.wisata_listbox.delete(0, tk.END)
        
        df = filtered_df if filtered_df is not None else self.df_hasil
        
        for idx, row in df.sort_values(['cluster', 'wisata']).iterrows():
            # Get emoji for kategori
            emoji = self.get_kategori_emoji(row['kategori'])
            
            # Format: emoji [Cluster] Nama - Kategori
            display_text = f"{emoji} [C{row['cluster']}] {row['wisata']}"
            
            self.wisata_listbox.insert(tk.END, display_text)
        
        # Update count
        self.count_label.config(text=f"Menampilkan: {len(df)} tempat")
    
    def filter_list(self, *args):
        """Filter list based on search query"""
        search_term = self.search_var.get().lower()
        
        # Start with full dataset
        filtered = self.df_hasil.copy()
        
        # Apply search filter
        if search_term:
            filtered = filtered[filtered['wisata'].str.lower().str.contains(search_term)]
        
        # Apply cluster filter
        if self.current_filter['cluster'] != 'all':
            filtered = filtered[filtered['cluster'] == self.current_filter['cluster']]
        
        # Apply kategori filter
        if self.current_filter['kategori'] != 'all':
            filtered = filtered[filtered['kategori'] == self.current_filter['kategori']]
        
        self.populate_listbox(filtered)
    
    def apply_filters(self, event=None):
        """Apply cluster and kategori filters"""
        # Get filter values
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
        self.filter_list()
        
        # Update status
        active_filters = []
        if self.current_filter['cluster'] != 'all':
            active_filters.append(f"Cluster {self.current_filter['cluster']}")
        if self.current_filter['kategori'] != 'all':
            active_filters.append(self.current_filter['kategori'])
        
        if active_filters:
            self.status_label.config(
                text=f"✅ Filter aktif: {', '.join(active_filters)}"
            )
        else:
            self.status_label.config(
                text="✅ Siap | Implementasi Custom: TF-IDF + K-Means (No Sklearn)"
            )
    
    def reset_filters(self):
        """Reset all filters to default"""
        self.cluster_filter.set('Semua')
        self.kategori_filter.set('Semua')
        self.search_var.set('')
        self.current_filter = {'cluster': 'all', 'kategori': 'all'}
        self.populate_listbox()
        self.status_label.config(
            text="✅ Filter direset | Menampilkan semua tempat"
        )
    
    def show_welcome_message(self):
        """Show welcome message when no selection"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        welcome_frame = tk.Frame(self.scrollable_frame, bg=self.colors['white'])
        welcome_frame.pack(fill='both', expand=True, pady=100)
        
        tk.Label(
            welcome_frame,
            text="👈",
            font=('Segoe UI', 60),
            bg=self.colors['white']
        ).pack()
        
        tk.Label(
            welcome_frame,
            text="Pilih tempat wisata di sebelah kiri",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['text']
        ).pack(pady=10)
        
        tk.Label(
            welcome_frame,
            text="untuk melihat detail analisis clustering",
            font=('Segoe UI', 12),
            bg=self.colors['white'],
            fg=self.colors['text_light']
        ).pack()
    
    def on_select_wisata(self, event):
        """Handle wisata selection from listbox"""
        selection = self.wisata_listbox.curselection()
        if not selection:
            return
        
        # Get selected text
        selected_text = self.wisata_listbox.get(selection[0])
        
        # Extract wisata name (remove emoji, cluster label)
        # Format: emoji [Cx] Nama
        parts = selected_text.split('] ', 1)
        if len(parts) > 1:
            wisata_name = parts[1].strip()
        else:
            wisata_name = selected_text.strip()
        
        # Show detail
        self.show_detail(wisata_name)
    
    def show_detail(self, wisata_name):
        """Show detail for selected wisata"""
        # Clear previous content
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Get wisata data
        wisata_data = self.df_hasil[self.df_hasil['wisata'] == wisata_name].iloc[0]
        reviews = self.df_raw[self.df_raw['wisata'] == wisata_name]['review'].tolist()
        
        # Update header
        self.detail_title.config(text=f"📍 {wisata_name}")
        
        # Main container
        main_container = tk.Frame(self.scrollable_frame, bg=self.colors['white'])
        main_container.pack(fill='both', expand=True, padx=25, pady=20)
        
        # Info cards section
        self.create_info_cards(main_container, wisata_data)
        
        # Reviews section
        self.create_reviews_section(main_container, reviews)
        
        # Update status
        self.status_label.config(text=f"✅ Menampilkan: {wisata_name}")
    
    def create_info_cards(self, parent, data):
        """Create information cards"""
        cards_container = tk.Frame(parent, bg=self.colors['white'])
        cards_container.pack(fill='x', pady=(0, 20))
        
        # Cluster Card
        self.create_card(
            cards_container,
            "🏷️ Cluster",
            f"Cluster {data['cluster']}",
            data['cluster_label'],
            self.colors['primary']
        ).pack(fill='x', pady=5)
        
        # Kategori Card
        self.create_card(
            cards_container,
            "⭐ Kategori",
            data['kategori'],
            self.get_kategori_description(data['kategori']),
            self.get_kategori_color(data['kategori'])
        ).pack(fill='x', pady=5)
        
        # Tema Card
        self.create_card(
            cards_container,
            "🎯 Tema Wisata",
            data['tema_utama'],
            f"Kategori: {data['tema_utama']}",
            self.colors['info']
        ).pack(fill='x', pady=5)
        
        # Kata Kunci Card with tags
        keywords_card = tk.Frame(cards_container, bg=self.colors['light'], relief='solid', bd=1)
        keywords_card.pack(fill='x', pady=5)
        
        # Header
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
        for keyword in keywords:
            tag = tk.Label(
                tags_frame,
                text=keyword,
                font=('Segoe UI', 10),
                bg=self.colors['secondary'],
                fg=self.colors['white'],
                padx=10,
                pady=5,
                relief='flat'
            )
            tag.pack(side='left', padx=3, pady=2)
    
    def create_card(self, parent, title, value, subtitle, color):
        """Create a styled info card"""
        card = tk.Frame(parent, bg=self.colors['light'], relief='solid', bd=1)
        
        # Card header
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
        
        # Card body
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
        """Create reviews section with all reviews"""
        reviews_section = tk.Frame(parent, bg=self.colors['white'])
        reviews_section.pack(fill='both', expand=True)
        
        # Section header
        header = tk.Frame(reviews_section, bg=self.colors['secondary'])
        header.pack(fill='x')
        
        tk.Label(
            header,
            text=f"💬 Review Pengunjung ({len(reviews)} review)",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['secondary'],
            fg=self.colors['white'],
            anchor='w'
        ).pack(fill='x', padx=15, pady=10)
        
        # Reviews container
        for idx, review in enumerate(reviews, 1):
            review_card = tk.Frame(
                reviews_section,
                bg=self.colors['light'],
                relief='solid',
                bd=1
            )
            review_card.pack(fill='x', pady=8)
            
            # Review number badge
            badge = tk.Label(
                review_card,
                text=f"#{idx}",
                font=('Segoe UI', 10, 'bold'),
                bg=self.colors['info'],
                fg=self.colors['white'],
                padx=10,
                pady=5
            )
            badge.pack(anchor='nw', padx=10, pady=10)
            
            # Review text
            review_text = tk.Label(
                review_card,
                text=review,
                font=('Segoe UI', 11),
                bg=self.colors['light'],
                fg=self.colors['text'],
                wraplength=700,
                justify='left',
                anchor='w'
            )
            review_text.pack(fill='x', padx=15, pady=(0, 15))
    
    def get_kategori_emoji(self, kategori):
        """Get emoji icon for kategori"""
        emoji_map = {
            'Sangat Baik': '⭐',
            'Baik': '👍',
            'Kurang Baik': '👎',
            'Netral': '➖'
        }
        return emoji_map.get(kategori, '📍')
    
    def get_kategori_color(self, kategori):
        """Get color for kategori"""
        color_map = {
            'Sangat Baik': self.colors['success'],
            'Baik': self.colors['secondary'],
            'Kurang Baik': self.colors['danger'],
            'Netral': self.colors['warning']
        }
        return color_map.get(kategori, self.colors['primary'])
    
    def get_kategori_description(self, kategori):
        """Get description for kategori"""
        desc_map = {
            'Sangat Baik': 'Tempat wisata dengan review sangat positif',
            'Baik': 'Tempat wisata dengan review positif',
            'Kurang Baik': 'Tempat wisata dengan review negatif',
            'Netral': 'Tempat wisata dengan review beragam'
        }
        return desc_map.get(kategori, 'Tidak ada deskripsi')


def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = WisataClusteringGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()