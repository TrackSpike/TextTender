# Text Tender: AI-Powered iMessage Autoresponder

Are you tired of having to interact with friends and family?

Text Tender is a Python-based application that integrates OpenAI's Chat GPT into Apple's Messages app, providing an intelligent and convenient autoresponder for your iMessages while you're away. Harnessing the power of cutting-edge language models, Text Tender ensures that your contacts receive timely, relevant, and engaging replies.

## Key Features

- Seamless integration with Apple's Messages app
- Powered by OpenAI's Chat GPT for natural, context-aware responses
- Customizable settings to adapt to your preferences
- Designed for macOS, requires a Mac to run

## Getting Started

To get started you need to create a `config.json` file in the root directory.

```json
{
  "OPENAI_API_KEY": "Your open AI key",
  "RECIPIENT_NUMBER": "+1xxxxxxxxxx",
  "YOUR_NUMBER": "+1xxxxxxxxxx",
  "SYSTEM_MESSAGE": "Pretend you are a person texting their friend. Respond to the messages as if you are texting.",
  "TEST_MODE": false,
  "CONTEXT_DEPTH": 10
}
```

## Contributing

We welcome contributions from the community! If you have a feature request, bug report, or want to contribute code, please feel free to open an issue or submit a pull request.

## Disclaimer

Text Tender utilizes OpenAI's Chat GPT, which is an AI language model. As such, it may occasionally produce unexpected or inappropriate responses. Please use Text Tender responsibly and always review its responses when possible. The developers of Text Tender are not responsible for any misuse or consequences arising from the use of this application.
