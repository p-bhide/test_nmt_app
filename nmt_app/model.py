import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from googletrans import Translator
from IndicTransToolkit.processor import IndicProcessor  # correct import


def translate(text, src_lang, tgt_lang, model):
    MODEL_NAME = model
    processor = IndicProcessor(inference=True)
    batch = processor.preprocess_batch(text, src_lang=src_lang, tgt_lang=tgt_lang)
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, trust_remote_code=True).to(DEVICE)

    inputs = tokenizer(
        batch,
        truncation=True, padding=True,
        return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        generated_tokens = model.generate(
            **inputs,
            max_length=256,
            num_beams=5,
            use_cache=False
        )

    decoded = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    translations = processor.postprocess_batch(decoded, lang=tgt_lang)
    return translations

def detect_src_lang(text, src_lang):
    translator = Translator()
    detection = translator.detect(text[0])
    languages = {
        'eng_Latn': 'en',
        'hin_Deva': 'hi',
        'mar_Deva': 'mr',
        'tam_Taml': 'ta',
        'ben_Beng': 'bn',
    }
    if detection.lang in [ 'en', 'hi', 'mr', 'ta', 'bn']:
        if languages.get(src_lang) == detection.lang:
            return "Correct Input Language..."
        else:
            return "Language Mismatch..."
    else:
        return "Unsupported Language..."
    


def translate_text(text, src_lang, tgt_lang):
    detect_src = detect_src_lang(text, src_lang)
    if 'correct'.lower() in detect_src.lower():
        if src_lang == 'eng_Latn':
            MODEL_NAME = "ai4bharat/indictrans2-en-indic-dist-200M"
            return translate(text, src_lang, tgt_lang, MODEL_NAME)
        elif tgt_lang == 'eng_Latn':
            MODEL_NAME = "ai4bharat/indictrans2-indic-en-dist-200M"
            return translate(text, src_lang, tgt_lang, MODEL_NAME)
        else:
            MODEL_NAME = "ai4bharat/indictrans2-indic-en-dist-200M"
            new_text = translate(text, src_lang, 'eng_Latn', MODEL_NAME)
            MODEL_NAME = "ai4bharat/indictrans2-en-indic-dist-200M"
            return translate(new_text, 'eng_Latn', tgt_lang, MODEL_NAME)
    else:
        return False, detect_src 