import numpy as np
import pandas as pd
import torch
from datasets import Dataset
from sklearn.model_selection import train_test_split
from transformers import (DistilBertForSequenceClassification,
                          DistilBertTokenizerFast, Trainer, TrainingArguments)


def clean_text(text):
    """Clean and preprocess the text"""
    if isinstance(text, str):
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    return ""

def prepare_dataset(data_path, sample_limit=1000):  # Increased sample limit
    """
    Prepare dataset from the hotel reviews CSV file.
    Expected CSV format: Hotel_Reviews.csv with columns:
    - Negative_Review
    - Positive_Review
    - Reviewer_Score
    """
    # Read the dataset
    reviews_df = pd.read_csv(data_path)
    
    # Limit the number of samples
    reviews_df = reviews_df.sample(n=min(sample_limit, len(reviews_df)), random_state=42)
    
    # Clean and combine positive and negative reviews
    reviews_df["review"] = reviews_df.apply(
        lambda x: clean_text(x["Negative_Review"]) + " " + clean_text(x["Positive_Review"]), 
        axis=1
    )
    
    # Create binary labels (1 for bad reviews, 0 for good reviews)
    reviews_df["is_bad_review"] = reviews_df["Reviewer_Score"].apply(lambda x: 1 if x < 5 else 0)
    
    # Select only relevant columns
    reviews_df = reviews_df[["review", "is_bad_review"]]
    
    # Remove empty reviews
    reviews_df = reviews_df[reviews_df["review"].str.strip() != ""]
    
    # Split into train and validation sets
    train_df, val_df = train_test_split(reviews_df, test_size=0.2, random_state=42)
    
    # Convert to HuggingFace datasets
    train_dataset = Dataset.from_pandas(train_df)
    val_dataset = Dataset.from_pandas(val_df)
    
    return train_dataset, val_dataset

def tokenize_function(examples, tokenizer):
    """Tokenize the texts and prepare labels"""
    tokenized = tokenizer(
        examples["review"],
        padding="max_length",
        truncation=True,
        max_length=512
    )
    
    # Add labels to the tokenized inputs
    tokenized["labels"] = examples["is_bad_review"]
    
    return tokenized

def main():
    # Configuration
    model_name = "distilbert-base-uncased"
    data_path = "./Hotel_Reviews.csv"
    output_dir = "fine_tuned_model"
    sample_limit = 1000  # Increased sample limit
    
    # Load tokenizer and model
    tokenizer = DistilBertTokenizerFast.from_pretrained(model_name)
    model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=2)
    
    # Prepare datasets with sample limit
    train_dataset, val_dataset = prepare_dataset(data_path, sample_limit=sample_limit)
    
    print(f"Training on {len(train_dataset)} samples")
    print(f"Validating on {len(val_dataset)} samples")
    
    # Tokenize datasets
    train_dataset = train_dataset.map(
        lambda x: tokenize_function(x, tokenizer),
        batched=True,
        remove_columns=train_dataset.column_names
    )
    val_dataset = val_dataset.map(
        lambda x: tokenize_function(x, tokenizer),
        batched=True,
        remove_columns=val_dataset.column_names
    )
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=5,  # Increased epochs
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir=f"{output_dir}/logs",
        logging_steps=100,
        evaluation_strategy="steps",
        eval_steps=500,
        save_strategy="steps",
        save_steps=500,
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        learning_rate=2e-5  # Added learning rate
    )
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
    )
    
    # Train the model
    trainer.train()
    
    # Save the model and tokenizer
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    print(f"Model saved to {output_dir}")

if __name__ == "__main__":
    main() 