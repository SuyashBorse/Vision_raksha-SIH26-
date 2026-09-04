# notebooks/train_local_cpu.py
# RetinAI - EfficientNet-B4 Training (CPU-optimized)
# Dataset: APTOS 2019 Blindness Detection
# Time: ~2-3 hours on CPU
#
# Usage:
#   cd D:\SIH26\dr-screening\backend
#   .\venv\Scripts\python.exe ..\notebooks\train_local_cpu.py

import os, gc, time, sys
import numpy as np
import pandas as pd
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import timm
from PIL import Image
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import cohen_kappa_score, classification_report
import albumentations as A
from albumentations.pytorch import ToTensorV2

# ================================================================
# CONFIG - Tuned for CPU training (~2-3 hours)
# ================================================================
CFG = {
    "model_name":   "efficientnet_b4",
    "img_size":     224,            # smaller than 380 for CPU speed
    "num_classes":  5,
    "epochs":       8,              # enough for good convergence
    "batch_size":   8,              # small batches for CPU RAM
    "lr":           3e-4,
    "weight_decay": 1e-4,
    "num_workers":  0,              # 0 for Windows compatibility
    "seed":         42,
    "device":       "cuda" if torch.cuda.is_available() else "cpu",
}

# Auto-detect dataset path
POSSIBLE_PATHS = [
    os.path.expanduser("~/.cache/kagglehub/competitions/aptos2019-blindness-detection"),
    os.path.expanduser("~/kagglehub/competitions/aptos2019-blindness-detection"),
    "D:/SIH26/datasets/aptos2019",
    "/kaggle/input/aptos2019-blindness-detection",
]

DATA_DIR = None
for base in POSSIBLE_PATHS:
    if os.path.exists(base):
        # Find the version folder (e.g., versions/1)
        for root, dirs, files in os.walk(base):
            if "train.csv" in files:
                DATA_DIR = root
                break
    if DATA_DIR:
        break

if DATA_DIR is None:
    print("ERROR: APTOS dataset not found. Download it first:")
    print("  python -c \"import kagglehub; kagglehub.competition_download('aptos2019-blindness-detection')\"")
    sys.exit(1)

MODEL_OUT = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                         "dr-screening", "models", "best_dr_model.pth")
os.makedirs(os.path.dirname(MODEL_OUT), exist_ok=True)

print(f"{'='*60}")
print(f"  RetinAI - DR Model Training")
print(f"  Device   : {CFG['device']}")
print(f"  Dataset  : {DATA_DIR}")
print(f"  Output   : {MODEL_OUT}")
print(f"  Img size : {CFG['img_size']}x{CFG['img_size']}")
print(f"  Epochs   : {CFG['epochs']}")
print(f"  Batch    : {CFG['batch_size']}")
print(f"{'='*60}")

# Seed
torch.manual_seed(CFG["seed"])
np.random.seed(CFG["seed"])

# ================================================================
# Dataset
# ================================================================
class APTOSDataset(Dataset):
    def __init__(self, df, img_dir, transform=None):
        self.df = df.reset_index(drop=True)
        self.img_dir = img_dir
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img_name = row["id_code"]

        # Try .png first, then .jpg
        img_path = os.path.join(self.img_dir, f"{img_name}.png")
        if not os.path.exists(img_path):
            img_path = os.path.join(self.img_dir, f"{img_name}.jpg")

        img = np.array(Image.open(img_path).convert("RGB"))

        if self.transform:
            img = self.transform(image=img)["image"]

        label = int(row["diagnosis"])
        return img, label


# ================================================================
# Augmentations
# ================================================================
def get_train_transform(size):
    return A.Compose([
        A.RandomResizedCrop(size, size, scale=(0.8, 1.0)),
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.5),
        A.RandomRotate90(p=0.5),
        A.CLAHE(clip_limit=2.0, p=0.3),
        A.ColorJitter(brightness=0.15, contrast=0.15, p=0.3),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])

def get_val_transform(size):
    return A.Compose([
        A.Resize(size, size),
        A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ToTensorV2(),
    ])


# ================================================================
# Training
# ================================================================
def train_epoch(model, loader, optimizer, criterion, device, epoch, total_epochs):
    model.train()
    total_loss, total = 0, 0
    start = time.time()

    for batch_idx, (imgs, labels) in enumerate(loader):
        imgs, labels = imgs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(imgs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * len(labels)
        total += len(labels)

        # Progress every 20 batches
        if (batch_idx + 1) % 20 == 0:
            elapsed = time.time() - start
            eta = elapsed / (batch_idx + 1) * (len(loader) - batch_idx - 1)
            print(f"  Epoch {epoch+1}/{total_epochs} | "
                  f"Batch {batch_idx+1}/{len(loader)} | "
                  f"Loss: {total_loss/total:.4f} | "
                  f"ETA: {eta/60:.1f}min", flush=True)

    return total_loss / total


def val_epoch(model, loader, criterion, device):
    model.eval()
    total_loss, total = 0, 0
    all_preds, all_labels = [], []

    with torch.no_grad():
        for imgs, labels in loader:
            imgs, labels = imgs.to(device), labels.to(device)
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            total_loss += loss.item() * len(labels)
            total += len(labels)
            preds = outputs.argmax(dim=1).cpu().numpy()
            all_preds.extend(preds)
            all_labels.extend(labels.cpu().numpy())

    kappa = cohen_kappa_score(all_labels, all_preds, weights="quadratic")
    return total_loss / total, kappa, all_preds, all_labels


# ================================================================
# Main
# ================================================================
def main():
    train_csv = os.path.join(DATA_DIR, "train.csv")
    train_df  = pd.read_csv(train_csv)

    # Find images directory
    img_dir = os.path.join(DATA_DIR, "train_images")
    if not os.path.exists(img_dir):
        # Sometimes images are in the same folder
        img_dir = DATA_DIR

    print(f"\nDataset: {len(train_df)} images")
    print(f"Images dir: {img_dir}")
    print(f"Grade distribution:")
    print(train_df["diagnosis"].value_counts().sort_index().to_string())
    print()

    # Class weights for imbalance
    counts  = train_df["diagnosis"].value_counts().sort_index().values.astype(float)
    weights = torch.tensor(1.0 / counts, dtype=torch.float)
    weights = weights / weights.sum() * len(counts)   # normalize
    weights = weights.to(CFG["device"])
    criterion = nn.CrossEntropyLoss(weight=weights)

    # Single fold for speed
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=CFG["seed"])
    train_idx, val_idx = next(iter(skf.split(train_df, train_df["diagnosis"])))

    print(f"Train: {len(train_idx)} | Val: {len(val_idx)}")

    train_ds = APTOSDataset(train_df.iloc[train_idx], img_dir,
                            get_train_transform(CFG["img_size"]))
    val_ds   = APTOSDataset(train_df.iloc[val_idx], img_dir,
                            get_val_transform(CFG["img_size"]))

    train_loader = DataLoader(train_ds, batch_size=CFG["batch_size"],
                              shuffle=True, num_workers=CFG["num_workers"])
    val_loader   = DataLoader(val_ds, batch_size=CFG["batch_size"],
                              shuffle=False, num_workers=CFG["num_workers"])

    # Model
    model = timm.create_model(CFG["model_name"], pretrained=True,
                              num_classes=CFG["num_classes"])
    model = model.to(CFG["device"])

    param_count = sum(p.numel() for p in model.parameters()) / 1e6
    print(f"Model: {CFG['model_name']} | {param_count:.1f}M params\n")

    optimizer = optim.AdamW(model.parameters(), lr=CFG["lr"],
                            weight_decay=CFG["weight_decay"])
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=CFG["epochs"])

    best_kappa = 0
    training_start = time.time()

    for epoch in range(CFG["epochs"]):
        epoch_start = time.time()

        train_loss = train_epoch(model, train_loader, optimizer, criterion,
                                 CFG["device"], epoch, CFG["epochs"])
        val_loss, kappa, preds, labels = val_epoch(model, val_loader, criterion,
                                                    CFG["device"])
        scheduler.step()

        epoch_time = time.time() - epoch_start
        total_time = time.time() - training_start
        remaining  = epoch_time * (CFG["epochs"] - epoch - 1)

        marker = ""
        if kappa > best_kappa:
            best_kappa = kappa
            torch.save(model.state_dict(), MODEL_OUT)
            marker = " << BEST - SAVED"

        print(f"Epoch {epoch+1:2d}/{CFG['epochs']} | "
              f"Train: {train_loss:.4f} | "
              f"Val: {val_loss:.4f} | "
              f"Kappa: {kappa:.4f} | "
              f"Time: {epoch_time/60:.1f}min | "
              f"ETA: {remaining/60:.0f}min"
              f"{marker}",
              flush=True)

    # Final report
    total_time = time.time() - training_start
    print(f"\n{'='*60}")
    print(f"  Training Complete!")
    print(f"  Total time  : {total_time/3600:.1f} hours")
    print(f"  Best Kappa  : {best_kappa:.4f}")
    print(f"  Model saved : {MODEL_OUT}")
    print(f"{'='*60}")

    # Classification report on best model
    model.load_state_dict(torch.load(MODEL_OUT, map_location=CFG["device"]))
    _, _, final_preds, final_labels = val_epoch(model, val_loader, criterion, CFG["device"])
    print("\nClassification Report:")
    labels_names = ["No DR", "Mild DR", "Moderate DR", "Severe DR", "Proliferative DR"]
    print(classification_report(final_labels, final_preds, target_names=labels_names))

    print("\nRestart your backend to use the trained model:")
    print("  cd D:\\SIH26\\dr-screening\\backend")
    print("  .\\venv\\Scripts\\uvicorn.exe main:app --host 0.0.0.0 --port 8000 --reload")


if __name__ == "__main__":
    main()
