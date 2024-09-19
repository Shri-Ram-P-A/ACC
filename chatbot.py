import google.generativeai as genai

class GenAIException(Exception):
    """GenAI Exception base class"""
    pass

class ChatBot:
    CHATBOT_NAME = "My Gemini AI"

    def __init__(self, api_key):
        self.genai = genai
        self.genai.configure(api_key=api_key)
        self.model_name = None
        self.conversation = None
        self._conversation_history = []

        self.list_available_models()  # Call to list available models
        self.preload_conversation()

    def list_available_models(self):
        try:
            models = self.genai.list_models()
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    self.model_name = model.name  # Select first valid model
                    break
        except Exception as e:
            raise GenAIException(f"Error listing models: {str(e)}")

    def send_prompt(self, prompt, temperature=0.1):
        if not self.conversation:
            raise GenAIException("No active conversation.")
        if not prompt:
            raise GenAIException("Prompt cannot be empty.")
        try:
            response = self.conversation.send_message(
                content=prompt,
                generation_config=self._generative_config(temperature),
            )
            response.resolve()
            return response.text  # Return just the response text
        except Exception as e:
            raise GenAIException(str(e))

    def start_conversation(self):
        if self.model_name:
            self.conversation = self.genai.GenerativeModel(self.model_name).start_chat(history=self._conversation_history)
        else:
            raise GenAIException('No valid model selected')

    def _generative_config(self, temperature):
        return genai.types.GenerationConfig(temperature=temperature)

    def _construct_message(self, text, role='user'):
        # Ensure the message format is as expected
        return {
            'role': role,
            'parts': [{'text': text}]
        }

    def preload_conversation(self, conversation_history=None):
        if conversation_history:
            self._conversation_history = [self._construct_message(msg['text'], msg['role']) for msg in conversation_history]
        else:
            self._conversation_history = [
                self._construct_message(
                    'From now on, return the output as a JSON object that can be loaded in Python with the key as \'text\'. For example, {"text": "<output goes here>"}',
                    'model'
                ),
                self._construct_message(
                    '{"text": "Sure, I can return the output as a regular JSON object with the key as \\"text\\". Here is an example: {\\"text\\": \\"Your Output\\"}.", "role": "model"}',
                    'model'
                )
            ]
