import google.generativeai as genai

genai.configure(api_key="AIzaSyAVkL3nXawu15SXAPFuVuYcA7_nP21Sktg")

models = genai.list_models()

for model in models:
    print(f"📦 {model.name} => {model.supported_generation_methods}")
