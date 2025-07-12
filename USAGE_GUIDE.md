# 🚀 Multi-LLM Query Tool - Complete Usage Guide

## 📁 Project Structure

```
multillm/
├── main.py              # Main CLI application
├── config.py            # Configuration and LLM settings
├── llm_clients.py       # LLM client implementations
├── setup.py             # Automated setup script
├── test_demo.py         # Demo script (no API keys required)
├── requirements.txt     # Python dependencies
├── env_example.txt      # Environment file template
├── quick_start.bat      # Windows quick setup
├── quick_start.sh       # Unix/Linux quick setup
├── README.md            # Main documentation
├── USAGE_GUIDE.md       # This file
└── .gitignore           # Git ignore file
```

## 🎯 What This Tool Does

1. **Takes your prompt** and sends it to 4-5 state-of-the-art LLMs simultaneously
2. **Collects all responses** from each LLM concurrently (faster than sequential)
3. **Uses GPT-4 as a judge** to evaluate each response for quality and accuracy
4. **Merges the best elements** from all responses into a comprehensive answer
5. **Presents the result** in a beautiful terminal interface

## 🔧 Setup Instructions

### Option 1: Quick Setup (Windows)
```bash
# Double-click quick_start.bat or run:
quick_start.bat
```

### Option 2: Quick Setup (Unix/Linux)
```bash
chmod +x quick_start.sh
./quick_start.sh
```

### Option 3: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create environment file
cp env_example.txt .env

# Edit .env with your API keys
# Then run:
python main.py --setup
```

## 🔑 Required API Keys

**At minimum, you need:**
- OpenAI API key (required for the judge LLM)

**Optional (the more you have, the better):**
- Anthropic API key (for Claude)
- Google API key (for Gemini)
- Cohere API key (for Command-R)

Add them to your `.env` file:
```env
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here
GOOGLE_API_KEY=your-google-key-here
COHERE_API_KEY=your-cohere-key-here
```

## 💡 Usage Examples

### Basic Query
```bash
python main.py -p "Explain quantum computing"
```

### Show Individual Responses
```bash
python main.py -p "What is machine learning?" --show-individual
```

### Interactive Mode
```bash
python main.py --interactive
```

### Get Setup Help
```bash
python main.py --setup
```

### View Demo (No API Keys Required)
```bash
python test_demo.py
```

## 🎨 Sample Output

```
🤖 Multi-LLM Query Tool
╭─────────────────────────────────────────────────────────────╮
│        Query multiple AI models and get the best           │
│              merged response automatically                  │
╰─────────────────────────────────────────────────────────────╯

🔍 Querying 4 LLMs...
📊 Evaluating and merging responses...

🎯 Final Merged Response:

## Evaluation
OpenAI GPT-4 provided excellent technical accuracy...
Anthropic Claude offered clear analogies...
Google Gemini gave comprehensive examples...

## Final Response
[Comprehensive merged response combining best elements]

## Reasoning
The final response combines GPT-4's technical precision,
Claude's accessibility, and Gemini's practical examples...

⏱️ Query completed in 12.34 seconds
```

## ⚡ Performance Features

- **Concurrent Processing**: All LLMs queried simultaneously
- **Intelligent Caching**: Avoids duplicate requests
- **Error Handling**: Graceful failure recovery
- **Progress Indicators**: Real-time status updates
- **Rich Terminal UI**: Beautiful, colorful output

## 🔧 Customization

### Adding New LLMs
Edit `config.py` to add new LLM configurations:

```python
LLMConfig(
    name="New LLM",
    api_key_env="NEW_LLM_API_KEY",
    model="model-name",
    max_tokens=4000,
    temperature=0.7
)
```

### Adjusting Evaluation Prompt
Modify `EVALUATION_PROMPT` in `config.py` to change how responses are evaluated.

### Changing Judge LLM
Update `JUDGE_LLM` in `config.py` to use a different model as the evaluator.

## 📊 Supported Models

| Provider | Model | Purpose |
|----------|--------|---------|
| OpenAI | GPT-4 Turbo | Primary + Judge |
| OpenAI | GPT-3.5 Turbo | Fast responses |
| Anthropic | Claude-3 Sonnet | Reasoning |
| Google | Gemini Pro | Multimodal |
| Cohere | Command-R Plus | Enterprise |

## 🐛 Troubleshooting

### "No LLMs enabled"
- Check your `.env` file has API keys
- Verify API keys are valid
- Ensure at least OpenAI key is present

### "Module not found"
- Run `pip install -r requirements.txt`
- Check Python version (3.8+ required)

### "API Error"
- Verify API key format
- Check rate limits on your accounts
- Ensure internet connectivity

### "Judge LLM not configured"
- OpenAI API key is required for the judge
- Check `OPENAI_API_KEY` in `.env`

## 🚀 Advanced Usage

### Batch Processing
```python
# For multiple queries, use the engine directly
from llm_clients import MultiLLMQueryEngine

engine = MultiLLMQueryEngine()
queries = ["Query 1", "Query 2", "Query 3"]

for query in queries:
    result = await engine.process_query(query)
    print(result["final_response"])
```

### Custom Evaluation
```python
# Modify evaluation logic in llm_clients.py
# Or create custom evaluation prompts
```

## 🎯 Best Practices

1. **Use specific prompts** for better results
2. **Enable all LLMs** you have access to
3. **Use interactive mode** for multiple queries
4. **Check individual responses** when debugging
5. **Keep API keys secure** (never commit to git)

## 🔄 Updates and Maintenance

- **Models**: Update model names in `config.py` as new versions release
- **Dependencies**: Run `pip install -r requirements.txt --upgrade` periodically
- **API Keys**: Rotate keys regularly for security

## 🤝 Contributing

To contribute:
1. Fork the repository
2. Add new LLM providers in `llm_clients.py`
3. Update configuration in `config.py`
4. Test thoroughly
5. Submit pull request

## 📝 License

This project is open source. Feel free to use, modify, and distribute.

---

**Happy querying with multiple LLMs!** 🎉 