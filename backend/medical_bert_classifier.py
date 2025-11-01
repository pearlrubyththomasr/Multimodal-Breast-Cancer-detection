import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel, get_linear_schedule_with_warmup
from torch.optim import AdamW
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple
import warnings
warnings.filterwarnings('ignore')

class MedicalBERTClassifier:
    def __init__(self, model_name='bert-base-uncased', num_labels=5):
        self.model_name = model_name
        self.num_labels = num_labels
        self.tokenizer = None
        self.model = None
        self.classifier = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # Medical entity labels for breast cancer - SIMPLIFIED to binary classification
        self.label_map = {
            'symptom_severity': 0,      # 0: mild, 1: moderate/severe
            'urgency_level': 1,         # 0: routine, 1: urgent/emergent
            'cancer_type_suspicion': 2, # 0: benign, 1: suspicious/malignant
            'treatment_discussion': 3,  # 0: no, 1: yes
            'family_history': 4         # 0: no, 1: yes
        }

    def initialize_model(self):
        """Initialize BERT model and tokenizer"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModel.from_pretrained(self.model_name)

            # Add classification head
            self.classifier = nn.Sequential(
                nn.Dropout(0.3),
                nn.Linear(self.model.config.hidden_size, 256),
                nn.ReLU(),
                nn.Dropout(0.2),
                nn.Linear(256, len(self.label_map))  # 5 outputs for binary classification
            )

            self.model.to(self.device)
            self.classifier.to(self.device)
            print(f"Initialized BERT model on {self.device}")

        except Exception as e:
            print(f"Error loading BERT model: {e}")
            raise e

    def generate_synthetic_medical_text(self, num_samples=1000):
        """Generate synthetic clinical notes for fine-tuning with BINARY labels"""
        symptoms = [
            "patient presents with breast pain and palpable lump",
            "mammogram shows suspicious mass requiring biopsy",
            "patient reports nipple discharge and skin changes",
            "family history of breast cancer in mother and sister",
            "urgent evaluation needed for rapidly growing mass",
            "routine follow-up for benign fibroadenoma",
            "post-menopausal woman with new breast tenderness",
            "patient concerned about genetic risk factors",
            "imaging reveals probable ductal carcinoma",
            "discussed chemotherapy and surgical options"
        ]

        synthetic_data = []

        for i in range(num_samples):
            base_text = np.random.choice(symptoms)

            # Add variations
            variations = []
            if "pain" in base_text:
                variations.append(f"severity {np.random.choice(['mild', 'moderate', 'severe'])}")
            if "mass" in base_text or "suspicious" in base_text:
                variations.append(f"assessment {np.random.choice(['benign', 'suspicious', 'malignant'])}")
            if "urgent" not in base_text and np.random.random() > 0.7:
                variations.append(f"priority {np.random.choice(['routine', 'urgent', 'emergent'])}")

            # Add 1-3 variations
            if variations:
                base_text += ", " + ", ".join(np.random.choice(variations, size=min(len(variations), 2), replace=False))

            # Create BINARY labels (0 or 1 only)
            labels = self._generate_binary_labels(base_text)

            synthetic_data.append({
                'text': base_text,
                'labels': labels
            })

        return pd.DataFrame(synthetic_data)

    def _generate_binary_labels(self, text):
        """Generate BINARY labels (0 or 1 only) to avoid CUDA errors"""
        text_lower = text.lower()

        # Symptom severity: 0=mild, 1=moderate/severe
        symptom_severity = 1 if any(term in text_lower for term in ['moderate', 'severe']) else 0

        # Urgency level: 0=routine, 1=urgent/emergent
        urgency_level = 1 if any(term in text_lower for term in ['urgent', 'emergent']) else 0

        # Cancer suspicion: 0=benign, 1=suspicious/malignant
        cancer_suspicion = 1 if any(term in text_lower for term in ['suspicious', 'malignant', 'carcinoma']) else 0

        # Treatment discussion: 0=no, 1=yes
        treatment_discussion = 1 if any(term in text_lower for term in ['chemotherapy', 'surgery', 'radiation', 'treatment', 'discussed']) else 0

        # Family history: 0=no, 1=yes
        family_history = 1 if 'family history' in text_lower else 0

        return [symptom_severity, urgency_level, cancer_suspicion, treatment_discussion, family_history]

    def prepare_datasets(self, df, train_ratio=0.8):
        """Prepare training and validation datasets"""
        from sklearn.model_selection import train_test_split

        train_df, val_df = train_test_split(df, train_size=train_ratio, random_state=42)

        train_dataset = self._create_dataset(train_df)
        val_dataset = self._create_dataset(val_df)

        return train_dataset, val_dataset

    def _create_dataset(self, df):
        """Create torch dataset from dataframe"""
        class MedicalDataset(torch.utils.data.Dataset):
            def __init__(self, texts, labels, tokenizer, max_len=128):
                self.texts = texts
                self.labels = labels
                self.tokenizer = tokenizer
                self.max_len = max_len

            def __len__(self):
                return len(self.texts)

            def __getitem__(self, idx):
                text = str(self.texts[idx])
                labels = self.labels[idx]

                encoding = self.tokenizer.encode_plus(
                    text,
                    add_special_tokens=True,
                    max_length=self.max_len,
                    padding='max_length',
                    truncation=True,
                    return_attention_mask=True,
                    return_tensors='pt',
                )

                return {
                    'input_ids': encoding['input_ids'].flatten(),
                    'attention_mask': encoding['attention_mask'].flatten(),
                    'labels': torch.tensor(labels, dtype=torch.float)  # CHANGED to float for BCE loss
                }

        texts = df['text'].values
        labels = list(df['labels'].values)
        return MedicalDataset(texts, labels, self.tokenizer)

    def train(self, num_epochs=3, batch_size=8, learning_rate=2e-5):  # Reduced batch size
        """Fine-tune BERT on medical text with FIXED training"""
        if self.model is None or self.tokenizer is None:
            self.initialize_model()

        # Generate synthetic data
        print("Generating synthetic medical text data...")
        synthetic_df = self.generate_synthetic_medical_text(500)  # Reduced for stability

        print(f"Generated {len(synthetic_df)} samples")
        train_dataset, val_dataset = self.prepare_datasets(synthetic_df)

        train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=batch_size)

        # Optimizer - include both model and classifier parameters
        optimizer = AdamW(list(self.model.parameters()) + list(self.classifier.parameters()), lr=learning_rate)
        total_steps = len(train_loader) * num_epochs
        scheduler = get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=0,
            num_training_steps=total_steps
        )

        # Use BCEWithLogitsLoss for multi-label binary classification
        loss_fn = nn.BCEWithLogitsLoss()

        # Training loop
        self.model.train()
        self.classifier.train()

        for epoch in range(num_epochs):
            total_loss = 0
            for batch_idx, batch in enumerate(train_loader):
                optimizer.zero_grad()

                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['labels'].to(self.device)

                # BERT forward pass
                outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
                pooled_output = outputs.last_hidden_state[:, 0, :]  # [CLS] token

                # Classification
                logits = self.classifier(pooled_output)

                # SINGLE loss calculation for multi-label binary classification
                loss = loss_fn(logits, labels)

                loss.backward()
                torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
                torch.nn.utils.clip_grad_norm_(self.classifier.parameters(), 1.0)
                optimizer.step()
                scheduler.step()

                total_loss += loss.item()

                if batch_idx % 20 == 0:
                    print(f'  Batch {batch_idx}, Loss: {loss.item():.4f}')

            avg_loss = total_loss / len(train_loader)
            print(f'Epoch {epoch + 1}/{num_epochs}, Average Loss: {avg_loss:.4f}')

            # Simple validation
            self.simple_validate(val_loader)

        print("Training completed!")

    def simple_validate(self, val_loader):
        """Simple validation without complex metrics"""
        self.model.eval()
        self.classifier.eval()

        total_loss = 0
        with torch.no_grad():
            for batch in val_loader:
                input_ids = batch['input_ids'].to(self.device)
                attention_mask = batch['attention_mask'].to(self.device)
                labels = batch['labels'].to(self.device)

                outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
                pooled_output = outputs.last_hidden_state[:, 0, :]
                logits = self.classifier(pooled_output)

                loss_fn = nn.BCEWithLogitsLoss()
                loss = loss_fn(logits, labels)
                total_loss += loss.item()

        avg_val_loss = total_loss / len(val_loader)
        print(f'  Validation Loss: {avg_val_loss:.4f}')

        self.model.train()
        self.classifier.train()

    def save_model(self, filepath):
        """Save the trained model"""
        model_data = {
            'model_state': self.model.state_dict(),
            'classifier_state': self.classifier.state_dict(),
            'tokenizer': self.tokenizer,
            'label_map': self.label_map,
            'model_config': {
                'model_name': self.model_name,
                'num_labels': self.num_labels
            }
        }
        torch.save(model_data, filepath)
        print(f"Model saved to {filepath}")

    def load_model(self, filepath):
        """Load model from file"""
        model_data = torch.load(filepath, map_location=self.device)
        self.initialize_model()
        self.model.load_state_dict(model_data['model_state'])
        self.classifier.load_state_dict(model_data['classifier_state'])
        self.tokenizer = model_data['tokenizer']
        self.label_map = model_data['label_map']
        print(f"Model loaded from {filepath}")

    def predict(self, clinical_text):
        """Predict medical entities from clinical text"""
        if self.model is None or self.tokenizer is None:
            raise ValueError("Model not initialized. Please load a trained model first.")

        self.model.eval()
        self.classifier.eval()

        with torch.no_grad():
            encoding = self.tokenizer.encode_plus(
                clinical_text,
                add_special_tokens=True,
                max_length=128,
                padding='max_length',
                truncation=True,
                return_attention_mask=True,
                return_tensors='pt',
            )

            input_ids = encoding['input_ids'].to(self.device)
            attention_mask = encoding['attention_mask'].to(self.device)

            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            pooled_output = outputs.last_hidden_state[:, 0, :]
            logits = self.classifier(pooled_output)

            # Get probabilities using sigmoid for binary classification
            probabilities = torch.sigmoid(logits).squeeze().tolist()
            predictions = [1 if p > 0.5 else 0 for p in probabilities]

            result = self._decode_predictions(predictions, clinical_text, probabilities)
            return result

    def _decode_predictions(self, predictions, original_text, probabilities):
        """Convert binary predictions to readable medical analysis"""
        return {
            'clinical_text': original_text,
            'symptom_analysis': {
                'severity': 'moderate/severe' if predictions[0] == 1 else 'mild',
                'confidence': probabilities[0]
            },
            'clinical_urgency': {
                'level': 'urgent/emergent' if predictions[1] == 1 else 'routine',
                'rationale': self._generate_urgency_rationale(original_text, predictions[1]),
                'confidence': probabilities[1]
            },
            'cancer_assessment': {
                'suspicion_level': 'suspicious/malignant' if predictions[2] == 1 else 'benign',
                'key_findings': self._extract_key_phrases(original_text),
                'confidence': probabilities[2]
            },
            'treatment_context': {
                'discussed': 'yes' if predictions[3] == 1 else 'no',
                'mentioned_treatments': self._extract_treatment_mentions(original_text),
                'confidence': probabilities[3]
            },
            'risk_factors': {
                'family_history': 'yes' if predictions[4] == 1 else 'no',
                'genetic_risk_mentioned': 'BRCA' in original_text.upper() or 'genetic' in original_text.lower(),
                'confidence': probabilities[4]
            },
            'model_metadata': {
                'model_type': 'BERT-base fine-tuned',
                'fine_tuned_on': 'synthetic_medical_text',
                'inference_time': 'real_time'
            }
        }


    def _generate_urgency_rationale(self, text, urgency_level):
        """Generate rationale for urgency assessment"""
        rationales = {
            0: "Routine clinical findings without urgent indicators",
            1: "Suspicious findings or concerning symptoms requiring prompt evaluation"
        }
        return rationales.get(urgency_level, "Standard clinical assessment")

    def _extract_key_phrases(self, text):
        """Extract key medical phrases from text"""
        key_terms = [
            'mass', 'lump', 'pain', 'tenderness', 'discharge',
            'suspicious', 'malignant', 'benign', 'biopsy', 'mammogram'
        ]
        found_terms = [term for term in key_terms if term in text.lower()]
        return found_terms[:5]

    def _extract_treatment_mentions(self, text):
        """Extract mentioned treatments from text"""
        treatments = [
            'chemotherapy', 'radiation', 'surgery', 'mastectomy', 'lumpectomy',
            'hormone therapy', 'targeted therapy', 'immunotherapy'
        ]
        mentioned = [treatment for treatment in treatments if treatment in text.lower()]
        return mentioned

