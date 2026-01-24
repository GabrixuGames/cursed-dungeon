#!/bin/bash
# Script de configuración del entorno de desarrollo para Cursed Dungeon

echo "=================================="
echo "Cursed Dungeon - Setup Script"
echo "=================================="

# Verificar si Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 no está instalado"
    exit 1
fi

echo "✓ Python 3 encontrado: $(python3 --version)"

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
    echo "✓ Entorno virtual creado"
else
    echo "✓ Entorno virtual ya existe"
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "📦 Actualizando pip..."
pip install --upgrade pip -q

# Instalar dependencias
echo "📦 Instalando dependencias..."
pip install -r requirements.txt -q

echo ""
echo "=================================="
echo "✅ Configuración completada!"
echo "=================================="
echo ""
echo "Para activar el entorno virtual:"
echo "  source venv/bin/activate"
echo ""
echo "Para ejecutar el juego:"
echo "  python main.py"
echo ""
echo "Para ejecutar los tests:"
echo "  python tests/test_suite.py"
echo ""
echo "Para desactivar el entorno:"
echo "  deactivate"
echo ""
