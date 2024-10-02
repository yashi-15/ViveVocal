from dotenv import load_dotenv
import os

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient


def main():
    try:
        global speech_config
        global translation_config
        global ai_client

        # Get Configuration Settings
        load_dotenv()
        speech_key = os.getenv('SPEECH_KEY')
        speech_region = os.getenv('SPEECH_REGION')
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')

        # Create client using endpoint and key
        credential = AzureKeyCredential(ai_key)
        ai_client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)

        # Configure speech recognition
        speech_config = speech_sdk.SpeechConfig(speech_key, speech_region)
        speech_config.speech_recognition_language = 'en-US'
        print('Running speech sentiment analysis program..')

        # Get user input
        while True:
            user_input = input('\nType "start" to begin speech analysis\n').lower()
            if user_input == 'y':
                FindSentiment()
            else:
                break  

    except Exception as ex:
        print(ex)

def FindSentiment():

    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak now...")
    result = speech_recognizer.recognize_once_async().get()
    print('Recognized: "{}"'.format(result.text))

    # Sentiment analysis on the input speech
    sentimentAnalysis = ai_client.analyze_sentiment(documents=[result.text])[0]

    # Display the sentiment result
    print("\nSentiment: {}".format(sentimentAnalysis.sentiment))


    # Synthesize translation
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
    speak = speech_synthesizer.speak_text_async(sentimentAnalysis.sentiment).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)


if __name__ == "__main__":
    main()


# pip install azure-ai-textanalytics==5.3.0
# pip install python-dotenv
# pip install azure-cognitiveservices-speech==1.30.0