#!/usr/bin/env python3
"""
Multi-LLM Query Tool
Query multiple state-of-the-art LLMs and get the best merged response.
"""

import asyncio
import sys
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
import time
from typing import Dict, Any

from llm_clients import MultiLLMQueryEngine

console = Console()

def display_banner():
    """Display the application banner"""
    banner = """
    ╭─────────────────────────────────────────────────────────────╮
    │                    🤖 Multi-LLM Query Tool                  │
    │                                                             │
    │        Query multiple AI models and get the best           │
    │              merged response automatically                  │
    ╰─────────────────────────────────────────────────────────────╯
    """
    console.print(banner, style="bold blue")

def display_individual_responses(responses: Dict[str, tuple]):
    """Display individual responses from each LLM"""
    console.print("\n📋 Individual Responses:", style="bold yellow")
    
    for name, (response, error) in responses.items():
        if error:
            console.print(f"\n❌ {name}: {error}", style="bold red")
        else:
            # Truncate long responses for display
            display_response = response[:500] + "..." if len(response) > 500 else response
            panel = Panel(
                display_response,
                title=f"🤖 {name}",
                title_align="left",
                border_style="green" if not error else "red"
            )
            console.print(panel)

def display_final_response(final_response: str):
    """Display the final merged response"""
    console.print("\n🎯 Final Merged Response:", style="bold green")
    
    # Try to parse if it's markdown format
    try:
        md = Markdown(final_response)
        console.print(md)
    except:
        # Fallback to regular text
        panel = Panel(
            final_response,
            title="🎯 Best Response",
            title_align="left",
            border_style="bold green"
        )
        console.print(panel)

def display_summary(result: Dict[str, Any]):
    """Display query summary"""
    table = Table(title="Query Summary")
    table.add_column("Metric", style="bold")
    table.add_column("Value", style="cyan")
    
    table.add_row("Query", result["query"][:100] + "..." if len(result["query"]) > 100 else result["query"])
    table.add_row("LLMs Used", ", ".join(result["llms_used"]))
    table.add_row("Judge LLM", result["judge_llm"])
    
    successful_responses = sum(1 for _, (resp, err) in result["individual_responses"].items() if not err)
    table.add_row("Successful Responses", f"{successful_responses}/{len(result['individual_responses'])}")
    
    console.print(table)

@click.command()
@click.option('--prompt', '-p', help='Query prompt to send to all LLMs')
@click.option('--show-individual', '-i', is_flag=True, help='Show individual responses from each LLM')
@click.option('--interactive', is_flag=True, help='Run in interactive mode')
@click.option('--setup', is_flag=True, help='Show setup instructions')
def main(prompt, show_individual, interactive, setup):
    """Multi-LLM Query Tool - Query multiple AI models and get the best merged response."""
    
    if setup:
        show_setup_instructions()
        return
    
    display_banner()
    
    if interactive:
        run_interactive_mode()
    elif prompt:
        asyncio.run(process_single_query(prompt, show_individual))
    else:
        console.print("❌ Please provide a prompt with -p or use --interactive mode", style="bold red")
        console.print("Use --help for more options")

def show_setup_instructions():
    """Show setup instructions for API keys"""
    setup_text = """
# Multi-LLM Query Tool Setup

## Required API Keys

Create a `.env` file in the project directory with your API keys:

```
# OpenAI (Required for GPT models and judge)
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic (Optional)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Google (Optional)
GOOGLE_API_KEY=your_google_api_key_here

# Cohere (Optional)
COHERE_API_KEY=your_cohere_api_key_here
```

## API Key Sources

- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/
- **Google**: https://makersuite.google.com/app/apikey
- **Cohere**: https://dashboard.cohere.ai/api-keys

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py -p "Your question here"
python main.py --interactive
```

**Note**: At minimum, you need an OpenAI API key as it's used for the judge LLM.
    """
    
    md = Markdown(setup_text)
    console.print(md)

async def process_single_query(prompt: str, show_individual: bool = False):
    """Process a single query"""
    try:
        # Initialize the engine
        engine = MultiLLMQueryEngine()
        
        # Process the query with progress indicator
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("Processing query...", total=None)
            
            start_time = time.time()
            result = await engine.process_query(prompt)
            end_time = time.time()
        
        # Display results
        if show_individual:
            display_individual_responses(result["individual_responses"])
        
        display_final_response(result["final_response"])
        
        # Show summary
        console.print(f"\n⏱️  Query completed in {end_time - start_time:.2f} seconds", style="dim")
        
        if show_individual:
            console.print("\n" + "="*60)
            display_summary(result)
        
    except Exception as e:
        console.print(f"❌ Error: {str(e)}", style="bold red")
        console.print("💡 Use --setup to check configuration requirements")

def run_interactive_mode():
    """Run the tool in interactive mode"""
    console.print("🔄 Interactive Mode - Type 'quit' to exit", style="bold cyan")
    
    while True:
        try:
            prompt = console.input("\n[bold green]Enter your query:[/bold green] ")
            
            if prompt.lower() in ['quit', 'exit', 'q']:
                console.print("👋 Goodbye!", style="bold blue")
                break
            
            if not prompt.strip():
                continue
            
            # Ask for display options
            show_individual = console.input("Show individual responses? (y/N): ").lower().startswith('y')
            
            console.print("\n" + "="*60)
            asyncio.run(process_single_query(prompt, show_individual))
            console.print("="*60)
            
        except KeyboardInterrupt:
            console.print("\n👋 Goodbye!", style="bold blue")
            break
        except Exception as e:
            console.print(f"❌ Error: {str(e)}", style="bold red")

if __name__ == "__main__":
    main() 