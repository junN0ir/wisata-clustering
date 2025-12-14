import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

def load_results():
    """Load hasil clustering"""
    df = pd.read_csv("../outputs/hasil_cluster_per_tempat.csv")
    return df

def plot_cluster_distribution(df):
    """Plot distribusi tempat wisata per cluster"""
    plt.figure(figsize=(10, 6))
    
    cluster_counts = df['cluster'].value_counts().sort_index()
    colors = sns.color_palette("husl", len(cluster_counts))
    
    bars = plt.bar(cluster_counts.index, cluster_counts.values, color=colors, edgecolor='black', alpha=0.7)
    
    # Tambahkan label di atas bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.xlabel('Cluster', fontsize=12, fontweight='bold')
    plt.ylabel('Jumlah Tempat Wisata', fontsize=12, fontweight='bold')
    plt.title('Distribusi Tempat Wisata per Cluster', fontsize=14, fontweight='bold', pad=20)
    plt.xticks(cluster_counts.index)
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../outputs/cluster_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: cluster_distribution.png")
    plt.close()

def plot_sentiment_distribution(df):
    """Plot distribusi kategori sentimen"""
    plt.figure(figsize=(10, 6))
    
    sentiment_counts = df['kategori'].value_counts()
    colors = {'Sangat Baik': '#2ecc71', 'Baik': '#3498db', 
              'Kurang Baik': '#e74c3c', 'Netral': '#95a5a6'}
    
    bar_colors = [colors.get(cat, '#95a5a6') for cat in sentiment_counts.index]
    bars = plt.bar(range(len(sentiment_counts)), sentiment_counts.values, 
                   color=bar_colors, edgecolor='black', alpha=0.7)
    
    # Tambahkan label
    for i, bar in enumerate(bars):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.xlabel('Kategori', fontsize=12, fontweight='bold')
    plt.ylabel('Jumlah Tempat Wisata', fontsize=12, fontweight='bold')
    plt.title('Distribusi Kategori Sentimen', fontsize=14, fontweight='bold', pad=20)
    plt.xticks(range(len(sentiment_counts)), sentiment_counts.index, rotation=15)
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../outputs/sentiment_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: sentiment_distribution.png")
    plt.close()

def plot_tema_distribution(df):
    """Plot distribusi tema wisata"""
    plt.figure(figsize=(12, 6))
    
    tema_counts = df['tema_utama'].value_counts()
    colors = sns.color_palette("Set2", len(tema_counts))
    
    bars = plt.barh(range(len(tema_counts)), tema_counts.values, color=colors, 
                    edgecolor='black', alpha=0.7)
    
    # Tambahkan label
    for i, bar in enumerate(bars):
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2.,
                f' {int(width)}',
                ha='left', va='center', fontsize=11, fontweight='bold')
    
    plt.ylabel('Tema Wisata', fontsize=12, fontweight='bold')
    plt.xlabel('Jumlah Tempat Wisata', fontsize=12, fontweight='bold')
    plt.title('Distribusi Tema Wisata', fontsize=14, fontweight='bold', pad=20)
    plt.yticks(range(len(tema_counts)), tema_counts.index)
    plt.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('../outputs/tema_distribution.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: tema_distribution.png")
    plt.close()

def plot_cluster_heatmap(df):
    """Plot heatmap cluster vs tema"""
    plt.figure(figsize=(10, 6))
    
    # Buat crosstab
    ct = pd.crosstab(df['cluster'], df['tema_utama'])
    
    # Plot heatmap
    sns.heatmap(ct, annot=True, fmt='d', cmap='YlOrRd', 
                cbar_kws={'label': 'Jumlah Tempat'},
                linewidths=0.5, linecolor='gray')
    
    plt.xlabel('Tema Wisata', fontsize=12, fontweight='bold')
    plt.ylabel('Cluster', fontsize=12, fontweight='bold')
    plt.title('Heatmap: Cluster vs Tema Wisata', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('../outputs/cluster_tema_heatmap.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: cluster_tema_heatmap.png")
    plt.close()

def main():
    """Main function untuk generate semua visualisasi"""
    print("\n" + "="*60)
    print("MEMBUAT VISUALISASI HASIL CLUSTERING")
    print("="*60)
    
    print("\n[1/4] Loading data...")
    df = load_results()
    
    print("\n[2/4] Membuat plot distribusi cluster...")
    plot_cluster_distribution(df)
    
    print("\n[3/4] Membuat plot distribusi sentimen...")
    plot_sentiment_distribution(df)
    
    print("\n[4/4] Membuat plot distribusi tema...")
    plot_tema_distribution(df)
    
    print("\n[5/5] Membuat heatmap cluster vs tema...")
    plot_cluster_heatmap(df)
    
    print("\n" + "="*60)
    print("VISUALISASI SELESAI!")
    print("="*60)
    print("\nFile visualisasi tersimpan di folder '../outputs/':")
    print("  • cluster_distribution.png")
    print("  • sentiment_distribution.png")
    print("  • tema_distribution.png")
    print("  • cluster_tema_heatmap.png")

if __name__ == "__main__":
    main()