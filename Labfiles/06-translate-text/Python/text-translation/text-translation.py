# import namespaces
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem

from dotenv import load_dotenv
import os
import requests, json

def main():
    global translator_endpoint

    # Load environment variables
    load_dotenv()
    cog_key = os.getenv('COG_SERVICE_KEY')  # Replace with your actual Azure AI Translator key
    cog_region = os.getenv('COG_SERVICE_REGION')  # Replace with your actual Azure AI Translator region
    translator_endpoint = 'https://api.cognitive.microsofttranslator.com'   

    # Create client using endpoint and key
    credential = TranslatorCredential(cog_key, cog_region)
    client = TextTranslationClient(credential)

    try:
        # Analyze each text file in the reviews folder
        reviews_folder = 'reviews'
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print('\n-------------\n' + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            print('\n' + text)

            # Detect the language
            language = GetLanguage(client, text)
            print('Language:', language)

            # Translate if not already English
            if language != 'en':
                translation = Translate(client, text, language)
                print("\nTranslation:\n{}".format(translation))
                
    except Exception as ex:
        print(ex)

def GetLanguage(client, text):
    # Use the Azure AI Translator detect function
    input_text_elements = [InputTextItem(text=text)]
    detect_language_result = client.detect_language(content=input_text_elements)
    detected_language = detect_language_result[0].detected_language.language

    # Return the detected language
    return detected_language

def Translate(client, text, source_language):
    # Use the Azure AI Translator translate function
    input_text_elements = [InputTextItem(text=text)]
    translation_response = client.translate(content=input_text_elements, to=['en'])
    translation = translation_response[0].translations[0].text

    # Return the translation
    return translation

if __name__ == "__main__":
    main()
