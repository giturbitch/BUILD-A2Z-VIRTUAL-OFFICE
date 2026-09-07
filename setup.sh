#!/bin/bash

# Virtual AI Office Setup Script

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     🤖 Virtual AI Office Setup Script 🤖                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create environment file
echo ""
echo "Setting up environment configuration..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file - please edit with your credentials"
else
    echo "⚠️  .env file already exists"
fi

# Create database
echo ""
echo "Initializing database..."
python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine); print('✅ Database initialized')"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║             ✅ Setup Complete!                              ║"
echo "║                                                              ║"
echo "║  Next steps:                                                ║"
echo "║  1. Edit .env with your API keys                           ║"
echo "║  2. Run: python run.py                                      ║"
echo "║  3. Visit: http://localhost:8000/dashboard                 ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
