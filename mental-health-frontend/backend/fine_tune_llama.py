from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset

model_name = "meta-llama/Llama-3.3-70B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

dataset = load_dataset('json', data_files='fine_tuning_data.jsonl', split='train')

# Tokenization
def tokenize_function(examples):
    return tokenizer(examples['prompt'], truncation=True, padding="max_length", max_length=256)

tokenized_dataset = dataset.map(tokenize_function, batched=True)

training_args = TrainingArguments(
    output_dir="./fine_tuned_llama",
    per_device_train_batch_size=1,  # Reduced to prevent OOM
    num_train_epochs=1,
    learning_rate=2e-5,
    weight_decay=0.01,
    logging_dir="./logs",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

# Fine-tune the model
trainer.train()

# Save the fine-tuned model
model.save_pretrained("./fine_tuned_llama")
tokenizer.save_pretrained("./fine_tuned_llama")

print("✅ LLaMA model fine-tuned successfully!")
