#!/usr/bin/env python3
"""
Setup script for Multi-LLM Query Tool
"""

import subprocess
import sys
import os
import shutil

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False
    return True

def setup_env_file():
    """Set up environment file"""
    print("🔧 Setting up environment file...")
    if os.path.exists(".env"):
        print("⚠️  .env file already exists, skipping...")
        return True
    
    if os.path.exists("env_example.txt"):
        shutil.copy("env_example.txt", ".env")
        print("✅ Created .env file from template")
        print("📝 Please edit .env file with your API keys")
        return True
    else:
        # Create basic .env file
        with open(".env", "w") as f:
            f.write("# Multi-LLM Query Tool - API Keys\n")
            f.write("# Add your API keys below\n\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            f.write("ANTHROPIC_API_KEY=your_anthropic_api_key_here\n")
            f.write("GOOGLE_API_KEY=your_google_api_key_here\n")
            f.write("COHERE_API_KEY=your_cohere_api_key_here\n")
        print("✅ Created basic .env file")
        print("📝 Please edit .env file with your API keys")
        return True

def test_installation():
    """Test if installation works"""
    print("🧪 Testing installation...")
    try:
        # Test imports
        import openai
        import anthropic
        import google.generativeai
        import cohere
        import rich
        import click
        print("✅ All imports successful!")
        
        # Test configuration
        from config import Config
        print("✅ Configuration loaded successfully!")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main setup function"""
    print("🤖 Multi-LLM Query Tool Setup")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed during requirements installation")
        sys.exit(1)
    
    # Setup environment file
    if not setup_env_file():
        print("❌ Setup failed during environment setup")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("❌ Setup failed during testing")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run: python main.py --setup (for detailed instructions)")
    print("3. Run: python main.py -p \"Your question here\"")
    print("4. Or run: python main.py --interactive")

if __name__ == "__main__":
    main() 