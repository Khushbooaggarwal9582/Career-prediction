# React frontend for the existing Career Predictor

This folder adds a React + Vite frontend without changing the existing Flask/ML backend.

## Run

From this `frontend` folder:

```bash
npm install
npm run dev
```

The React app sends the existing prediction request to:

`http://127.0.0.1:5000/predict`

Start the existing backend separately from the project root:

```bash
python app.py
```

No model files, Flask routes, training code, or prediction logic were changed.
