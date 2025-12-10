#!/usr/bin/env python3
"""
Script pour télécharger une image de trafic ouest-africain libre de droits.
"""
import urllib.request
import os

# URLs d'images libres de droits de trafic africain (Wikimedia Commons / Unsplash)
IMAGES = {
    # Image de trafic Lagos depuis Unsplash (libre de droits)
    "traffic_lagos_motos.jpg": "https://images.unsplash.com/photo-1618828665011-0abd973f7bb8?w=1200&q=80",
    # Alternative: trafic africain générique
    "traffic_africa_alt.jpg": "https://images.unsplash.com/photo-1565193566173-7a0ee3dbe261?w=1200&q=80",
}

def download_image(url: str, filename: str):
    """Télécharge une image depuis une URL."""
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    filepath = os.path.join(assets_dir, filename)
    
    if os.path.exists(filepath):
        print(f"✓ {filename} existe déjà")
        return
    
    print(f"⬇ Téléchargement de {filename}...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        print(f"✓ {filename} téléchargé avec succès")
    except Exception as e:
        print(f"✗ Erreur pour {filename}: {e}")

def main():
    print("=== Téléchargement d'images de trafic ouest-africain ===\n")
    for filename, url in IMAGES.items():
        download_image(url, filename)
    print("\n=== Terminé ===")
    print("\nNote: Ces images proviennent d'Unsplash et sont libres de droits.")
    print("Vous pouvez les utiliser avec attribution: 'Photo by [Photographer] on Unsplash'")

if __name__ == "__main__":
    main()
