# 🤖 Multi-LLM Query Tool

A powerful tool that queries multiple state-of-the-art LLMs simultaneously, evaluates their responses, and presents the best merged answer automatically.

## ✨ Features

- **Multi-LLM Support**: Query 4-5 top LLMs simultaneously
- **Automatic Evaluation**: Uses GPT-4 as a judge to evaluate and merge responses
- **Rich CLI Interface**: Beautiful terminal interface with progress indicators
- **Interactive Mode**: Continuous querying without restarting
- **Error Handling**: Graceful handling of API failures
- **Configurable**: Easy to add/remove LLMs and adjust settings

## 🚀 Supported LLMs

- **OpenAI GPT-4 Turbo** (Latest)
- **Anthropic Claude-3 Sonnet**
- **Google Gemini Pro**
- **Cohere Command-R Plus**
- **OpenAI GPT-3.5 Turbo**

## 📋 Requirements

- Python 3.8+
- API keys for desired LLM providers
- At minimum: OpenAI API key (required for judge LLM)

## 🛠️ Installation

1. **Clone/Download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up API keys**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## 🔑 API Key Setup

Get your API keys from:
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/
- **Google**: https://makersuite.google.com/app/apikey
- **Cohere**: https://dashboard.cohere.ai/api-keys

Add them to your `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
```

## 💡 Usage

### Quick Query
```bash
python main.py -p "Explain quantum computing in simple terms"
```

### Interactive Mode
```bash
python main.py --interactive
```

### Show Individual Responses
```bash
python main.py -p "Your question" --show-individual
```

### Setup Help
```bash
python main.py --setup
```

## 📊 How It Works

1. **Query Phase**: Sends your prompt to all configured LLMs simultaneously
2. **Collection Phase**: Collects responses from each LLM
3. **Evaluation Phase**: Uses GPT-4 as a judge to analyze all responses
4. **Merging Phase**: Creates a comprehensive merged response combining the best elements
5. **Presentation Phase**: Shows you the final result with optional individual responses

## 🎯 Example Output

```
🔍 Querying 4 LLMs...
📊 Evaluating and merging responses...

🎯 Final Merged Response:
## Evaluation
GPT-4 provided comprehensive technical details...
Claude offered excellent analogies...
Gemini had strong practical examples...

## Final Response
Quantum computing is a revolutionary technology that...
[Merged response combining best elements]

## Reasoning
The final response combines GPT-4's technical accuracy,
Claude's clear explanations, and Gemini's practical examples...
```

## ⚙️ Configuration

Edit `config.py` to:
- Add/remove LLMs
- Adjust model parameters
- Change the judge LLM
- Modify evaluation prompts

## 🔧 Troubleshooting

**No LLMs enabled**: Ensure you have API keys in your `.env` file
**API errors**: Check your API keys and rate limits
**Installation issues**: Ensure Python 3.8+ and pip are properly installed

## 🚦 Performance

- **Concurrent queries**: All LLMs are queried simultaneously
- **Typical response time**: 10-30 seconds depending on LLM speeds
- **Rate limiting**: Respects each provider's rate limits

## 🤝 Contributing

Feel free to:
- Add support for new LLMs
- Improve the evaluation logic
- Enhance the CLI interface
- Add new features

## 📝 License

This project is open source. Feel free to use, modify, and distribute.

## 🆘 Support

For issues:
1. Check your API keys in `.env`
2. Run `python main.py --setup` for configuration help
3. Ensure all dependencies are installed

---

**Happy querying!** 🎉 