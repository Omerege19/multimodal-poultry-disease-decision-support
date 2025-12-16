# Multimodal Poultry Disease Decision Support System

This repository contains the source code of a multimodal hybrid AI-based decision support system developed for the early detection of common poultry diseases. The system integrates deep learning–based visual analysis with biologically informed decision logic to support both field-level awareness and laboratory-level diagnostic evaluation.

This repository accompanies an academic report written in Turkish and is provided for transparency, reproducibility, and academic evaluation purposes.

---

## Project Motivation

Poultry diseases often present overlapping visual symptoms across different biological systems, making reliable diagnosis based on a single visual cue unreliable. In particular, gastrointestinal and lesion-based diseases may share similar appearances while having distinct biological consequences and intervention priorities.

To address this limitation, this project adopts a **multi-module hybrid approach**, where different disease groups are analyzed using specialized deep learning models optimized for their respective biological characteristics.

---

## System Overview

The proposed system consists of two independent but complementary deep learning models:

- **Model-1** targets gastrointestinal system diseases using feces image analysis.
- **Model-2** targets external and lesion-based diseases using high-resolution visual analysis.

Each model is trained and optimized separately, and their outputs are designed to support a higher-level decision mechanism that prioritizes biologically critical cases and enables downstream validation (e.g., serological confirmation).

---

## Models

### Model-1: EfficientNet-B1–Based Gastrointestinal Disease Classification Model

- Architecture: EfficientNet-B1 (ImageNet pretrained)
- Input modality: Feces images
- Target classes:
  - Coccidiosis
  - Salmonella
  - Newcastle Disease
  - Healthy
- Design objective:
  - Lightweight architecture
  - Fast inference
  - Suitable for early screening and field-level deployment

This model emphasizes sensitivity (recall) for biologically critical gastrointestinal infections, where missed detections may lead to rapid disease spread.

---

### Model-2: EfficientNet-B4–Based Lesion Classification Model

- Architecture: EfficientNet-B4 (ImageNet pretrained)
- Input modality: Lesion and external morphology images
- Target classes:
  - Bumblefoot
  - Coryza
  - CRD
  - Fowlpox
  - Healthy
- Design objective:
  - Higher representational capacity
  - Improved discrimination of visually similar lesions
  - Optimized for detailed clinical evaluation

---

## Training Strategy

Both models follow a two-stage training protocol:

### Stage 1 – Feature Extractor Frozen
- Backbone (EfficientNet) weights are frozen.
- Only the classifier head is trained.
- Stabilizes learning and prevents catastrophic forgetting.

### Stage 2 – Fine-Tuning
- Selected tail blocks of the backbone are unfrozen.
- Lower learning rate is applied to pretrained layers.
- Improves performance on visually ambiguous disease classes.

Additional techniques applied during training:
- ImageNet mean–standard deviation normalization
- Data augmentation (rotation, cropping, color jitter)
- Random Erasing for regularization
- Class-weighted cross-entropy loss to address class imbalance
- Mixed precision training (AMP)
- Early stopping based on validation loss

---

## Dataset Structure

The code expects datasets to follow the standard `ImageFolder` directory structure:

