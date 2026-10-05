from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


MODEL_NAME = "facebook/nllb-200-distilled-600M"


def load_translation_model():

    print("Loading NLLB model...")

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_NAME
    )

    print("NLLB model loaded!")

    return tokenizer, model


def translate_text(
    tokenizer,
    model,
    text,
    source_language,
    target_language
):

    tokenizer.src_lang = source_language

    inputs = tokenizer(
        text,
        return_tensors="pt"
    )

    translated_tokens = model.generate(
        **inputs,
        forced_bos_token_id=(
            tokenizer.convert_tokens_to_ids(
                target_language
            )
        )
    )

    translation = tokenizer.batch_decode(
        translated_tokens,
        skip_special_tokens=True
    )[0]

    return translation
