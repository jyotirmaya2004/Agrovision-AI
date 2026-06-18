# Plant Leaf Disease Detection

A production-ready Streamlit web application that first validates whether an uploaded image is a plant leaf, then detects plant leaf diseases using a TensorFlow MobileNetV2 disease model. The app also provides disease guidance and an agriculture-only AI assistant powered by the NVIDIA API.

## Features

- TensorFlow Keras model loading with process-level caching
- Two-stage prediction: leaf-vs-non-leaf validation before disease classification
- JPG, JPEG, PNG, WEBP, BMP, GIF, TIFF, HEIC, and HEIF image upload support
- 224 x 224 image resizing for both validation and disease models
- Top 3 disease predictions with confidence scores
- Disease knowledge base for symptoms, causes, treatment, and prevention
- NVIDIA API chatbot with session memory and agriculture topic restriction
- Sidebar-free mobile-first layout with chat-style assistant input
- Modular prediction logic separated from the Streamlit UI

## Project Structure

```text
Plantexa AI/
├── app.py
├── backend/
│   ├── disease_info.py
│   ├── model_loader.py
│   └── predict_two_stage.py
├── frontend/
│   ├── chatbot.py
│   ├── components.py
│   ├── styles.py
│   └── ui.py
├── model/
│   ├── leaf_disease_model.keras
│   ├── leaf_vs_non_leaf_model.keras
│   └── class_names.json
├── pages/
├── test/
├── disease_info.json
├── requirements.txt
├── .env.example
└── README.md
```

## Installation

Open the project folder in VS Code or a terminal:

```bash
cd LeafDiseaseApp
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If you want reliable iPhone-style photo uploads, keep `pillow-heif` installed so HEIC and HEIF files can be decoded.

## NVIDIA API Configuration

Create a `.env` file in the project root using `.env.example` as the guide:

```env
NVIDIA_API_KEY=your_nvidia_api_key_here
NVIDIA_MODEL=meta/llama-3.1-70b-instruct
```

The chatbot uses NVIDIA's OpenAI-compatible endpoint:

```text
https://integrate.api.nvidia.com/v1
```

If `NVIDIA_API_KEY` is not configured, disease prediction still works, and the chatbot will show a friendly configuration message.

## Running Streamlit

Start the app locally:

```bash
streamlit run app.py
```

Streamlit will print a local URL, typically:

```text
http://localhost:8501
```

## How To Use

1. Upload a clear image of a single plant leaf in a common image format such as JPG, PNG, WEBP, BMP, GIF, or TIFF.
2. On mobile, switch to the camera capture option if gallery uploads are unstable.
3. Click **Analyze Leaf**.
4. The app checks whether the image looks like a leaf.
5. If leaf validation passes, review the predicted disease, confidence score, and top 3 predictions.
6. Read disease symptoms, causes, treatment, and prevention guidance.
7. Ask the AI assistant agriculture-related questions about plant health, fertilizers, pest control, and farming practices.

## Model Notes

The app expects:

- `model/leaf_disease_model.keras`
- `model/leaf_vs_non_leaf_model.keras`
- `model/class_names.json`

Images are resized to `224 x 224`.

The leaf validation model uses `1./255` rescaling and was trained as a binary classifier with `{'leaf': 0, 'non_leaf': 1}`. Because its final layer is `Dense(1, activation='sigmoid')`, lower output values mean leaf and higher output values mean non-leaf. The disease model runs only after the validation model reaches the leaf confidence threshold.

## Project Screenshots

Add screenshots of the running app to a `screenshots/` folder when documenting a deployment or submission:

- Upload and prediction screen
- Prediction result with top 3 table
- Disease knowledge base section
- AI assistant chat section

## Troubleshooting

- If TensorFlow fails to install, verify your Python version is supported by your TensorFlow release.
- If prediction fails, confirm both model files and the class names file are present in the `model/` directory.
- If the chatbot does not respond, check that `.env` contains a valid `NVIDIA_API_KEY` and restart Streamlit.
- If an uploaded file is rejected, confirm it is a valid image file and try again.
- If phone photos still fail, try the camera capture option or convert HEIC images to JPG if your browser cannot decode them.

## Future Improvements

- Add Grad-CAM heatmaps to explain model attention.
- Store prediction history in a database.
- Add multilingual disease guidance.
- Add location-aware crop treatment recommendations.
- Add confidence thresholds and uncertainty warnings.
- Package the app with Docker for easier deployment.
