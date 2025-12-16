"""
Launcher untuk GUI Clustering Wisata Balikpapan
Otomatis cek data dan jalankan clustering jika perlu
"""

import os
import sys
from pathlib import Path

def check_files():
    """Check apakah semua file yang dibutuhkan ada"""
    required_files = {
        'hasil': '../outputs/hasil_cluster_per_tempat.csv',
        'raw': '../data/raw/wisata_balikpapan.csv'
    }
    
    missing = []
    for name, path in required_files.items():
        if not Path(path).exists():
            missing.append((name, path))
    
    return missing

def run_clustering():
    """Jalankan clustering jika file hasil belum ada"""
    print("="*60)
    print("FILE HASIL CLUSTERING TIDAK DITEMUKAN")
    print("="*60)
    print("\nMenjalankan clustering terlebih dahulu...")
    print("Mohon tunggu...\n")
    
    try:
        import main
        print("\n✅ Clustering selesai!")
        return True
    except Exception as e:
        print(f"\n❌ Error saat menjalankan clustering: {e}")
        return False

def main():
    """Main launcher function"""
    print("\n" + "="*60)
    print("GUI LAUNCHER - Clustering Wisata Balikpapan")
    print("="*60 + "\n")
    
    # Check if running from correct directory
    if not os.path.exists('main.py'):
        print("❌ Error: Jalankan script ini dari folder 'src/'")
        print("\nCaranya:")
        print("  cd src")
        print("  python run_gui.py")
        input("\nTekan Enter untuk keluar...")
        sys.exit(1)
    
    # Check required files
    print("[1/3] Checking files...")
    missing = check_files()
    
    if missing:
        print("\n⚠️  File yang hilang:")
        for name, path in missing:
            print(f"   - {name}: {path}")
        
        if any(name == 'raw' for name, _ in missing):
            print("\n❌ Error: File data CSV tidak ditemukan!")
            print(f"   Letakkan 'wisata_balikpapan.csv' di folder 'data/raw/'")
            input("\nTekan Enter untuk keluar...")
            sys.exit(1)
        
        # File hasil tidak ada, jalankan clustering
        print("\n[2/3] Running clustering...")
        if not run_clustering():
            print("\n❌ Gagal menjalankan clustering!")
            input("\nTekan Enter untuk keluar...")
            sys.exit(1)
    else:
        print("   ✅ Semua file ditemukan!")
        print("\n[2/3] Skipping clustering (file sudah ada)")
    
    # Launch GUI
    print("\n[3/3] Meluncurkan GUI...")
    print("\n🚀 Membuka GUI Clustering Wisata Balikpapan...")
    print("   Fitur: Filter Cluster, Filter Kategori, Search, Statistics")
    
    try:
        import gui
        gui.main()
    except Exception as e:
        print(f"\n❌ Error saat menjalankan GUI: {e}")
        import traceback
        traceback.print_exc()
        input("\nTekan Enter untuk keluar...")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Program dihentikan oleh user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error tidak terduga: {e}")
        import traceback
        traceback.print_exc()
        input("\nTekan Enter untuk keluar...")
        sys.exit(1)