#!/usr/bin/env python3
"""
Demo script for Multi-LLM Query Tool
This script demonstrates the tool's functionality without requiring actual API keys.
"""

import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

def demo_banner():
    """Display demo banner"""
    banner = """
    ╭─────────────────────────────────────────────────────────────╮
    │                🚀 Multi-LLM Query Tool Demo                 │
    │                                                             │
    │     This demo shows how the tool works without API keys    │
    ╰─────────────────────────────────────────────────────────────╯
    """
    console.print(banner, style="bold blue")

def demo_query_process():
    """Demonstrate the query process"""
    console.print("\n🔍 Querying 4 LLMs...", style="yellow")
    
    # Simulate individual responses
    demo_responses = {
        "OpenAI GPT-4": "Quantum computing uses quantum bits (qubits) that can exist in superposition, allowing parallel processing of multiple states simultaneously. This enables exponential speedup for certain computational problems.",
        "Anthropic Claude": "Think of quantum computing like a magical coin that can be heads AND tails at the same time. Regular computers process information sequentially, but quantum computers can explore many possibilities simultaneously.",
        "Google Gemini": "Quantum computing leverages quantum mechanical phenomena like superposition and entanglement. Key applications include cryptography, drug discovery, and optimization problems that are intractable for classical computers.",
        "Cohere Command": "Quantum computing represents a paradigm shift from classical binary computing. It uses quantum gates to manipulate qubits, offering potential breakthroughs in machine learning and complex simulations."
    }
    
    console.print("\n📋 Individual Responses:", style="bold yellow")
    for name, response in demo_responses.items():
        panel = Panel(
            response,
            title=f"🤖 {name}",
            title_align="left",
            border_style="green"
        )
        console.print(panel)
    
    console.print("\n📊 Evaluating and merging responses...", style="yellow")
    
    # Simulate final merged response
    final_response = """
## Evaluation

**OpenAI GPT-4** provided excellent technical accuracy with proper terminology and clear explanation of superposition and parallel processing capabilities.

**Anthropic Claude** offered the most accessible analogy with the "magical coin" metaphor, making complex concepts understandable for general audiences.

**Google Gemini** gave comprehensive coverage of applications and real-world use cases, connecting theory to practical implementations.

**Cohere Command** emphasized the paradigm shift aspect and mentioned specific technical implementations with quantum gates.

## Final Response

**Quantum computing is a revolutionary computational paradigm that harnesses quantum mechanical phenomena to process information in fundamentally new ways.**

Unlike classical computers that use bits (0 or 1), quantum computers use **quantum bits (qubits)** that can exist in **superposition** - simultaneously being both 0 and 1, like a magical coin that's both heads and tails at once.

This unique property allows quantum computers to:
- **Process multiple possibilities simultaneously** rather than sequentially
- **Achieve exponential speedup** for certain types of problems
- **Explore vast solution spaces** through parallel quantum states

**Key Applications:**
- **Cryptography**: Breaking current encryption and creating quantum-safe security
- **Drug Discovery**: Simulating molecular interactions for new medicines
- **Optimization**: Solving complex logistics and scheduling problems
- **Machine Learning**: Accelerating AI training and pattern recognition

**Technical Implementation:**
Quantum computers use quantum gates to manipulate qubits, leveraging phenomena like entanglement where qubits become correlated in ways that have no classical equivalent.

## Reasoning

The final response combines:
- GPT-4's technical precision and terminology
- Claude's accessible analogies for general understanding  
- Gemini's comprehensive application examples
- Cohere's emphasis on the paradigm shift and technical implementation

This creates a response that is both technically accurate and accessible to different audience levels.
"""
    
    console.print("\n🎯 Final Merged Response:", style="bold green")
    md = Markdown(final_response)
    console.print(md)

def demo_features():
    """Show key features"""
    console.print("\n✨ Key Features:", style="bold cyan")
    
    features = [
        "🔄 **Concurrent Querying**: All LLMs queried simultaneously for speed",
        "🧠 **Intelligent Evaluation**: GPT-4 judge analyzes and merges responses",
        "🎨 **Rich Interface**: Beautiful terminal output with progress indicators",
        "🔧 **Configurable**: Easy to add/remove LLMs and adjust parameters",
        "🛡️ **Error Handling**: Graceful failure handling for API issues",
        "🔄 **Interactive Mode**: Continuous querying without restart"
    ]
    
    for feature in features:
        console.print(f"  {feature}")

def demo_usage():
    """Show usage examples"""
    console.print("\n💡 Usage Examples:", style="bold cyan")
    
    usage_examples = [
        "python main.py -p \"Explain machine learning\"",
        "python main.py --interactive",
        "python main.py -p \"Compare Python vs JavaScript\" --show-individual",
        "python main.py --setup"
    ]
    
    for example in usage_examples:
        console.print(f"  📝 {example}", style="dim")

def main():
    """Main demo function"""
    demo_banner()
    demo_query_process()
    demo_features()
    demo_usage()
    
    console.print("\n🎉 Ready to use the Multi-LLM Query Tool!", style="bold green")
    console.print("📋 Next steps:")
    console.print("1. Run: python setup.py")
    console.print("2. Edit .env file with your API keys")
    console.print("3. Start querying: python main.py -p \"Your question\"")

if __name__ == "__main__":
    main() 