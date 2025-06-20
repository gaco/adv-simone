#!/usr/bin/env python3
"""
Launcher script for Simone Persin Côrtes Portfolio
"""

import os
import sys


def main():
    """Main function to start the Flask application"""
    print("=" * 50)
    print("   PORTFÓLIO Simone Persin Côrtes - ADVOCACIA")
    print("=" * 50)
    print()
    print("Iniciando servidor Flask...")
    print()
    print("URLs disponíveis:")
    print("  • Portfólio:        http://localhost:5000")
    print("  • Painel Admin:     http://localhost:5000/admin")
    print()
    print("Pressione Ctrl+C para parar o servidor")
    print("=" * 50)
    print()

    # Import and run the Flask app
    from app import app

    app.run(debug=True, host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
