import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from sklearn.utils.class_weight import compute_class_weight
import numpy as np
import os

# =============================
# SAFETY: GPU MEMORY FIX
# =============================
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except:
        pass

# =============================
# DATA PATHS
# =============================
train_dir = "dataset/Training"
test_dir = "dataset/Testing"

IMG_SIZE = (224, 224)
BATCH_SIZE = 16

# =============================
# DATA GENERATORS (SAFE + CORRECT)
# =============================
train_gen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    rotation_range=15,
    zoom_range=0.15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    fill_mode="nearest"
)

test_gen = ImageDataGenerator(
    preprocessing_function=preprocess_input
)

train_data = train_gen.flow_from_directory(
    train_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=True
)

test_data = test_gen.flow_from_directory(
    test_dir,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    shuffle=False
)

# =============================
# CLASS WEIGHTS (ANTI-BIAS SAFETY)
# =============================
class_weights = compute_class_weight(
    class_weight='balanced',
    classes=np.unique(train_data.classes),
    y=train_data.classes
)

class_weights = dict(enumerate(class_weights))

# =============================
# RESNET50 BASE MODEL
# =============================
base_model = ResNet50(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

base_model.trainable = False  # Stage 1: freeze

# =============================
# CUSTOM HEAD (GRAD-CAM READY)
# =============================
inputs = tf.keras.Input(shape=(224, 224, 3))

x = base_model(inputs, training=False)

# IMPORTANT: Grad-CAM layer
x = layers.Conv2D(128, (3,3), activation='relu', name="last_conv")(x)

x = layers.GlobalAveragePooling2D()(x)
x = layers.Dense(128, activation='relu')(x)
x = layers.Dropout(0.5)(x)

outputs = layers.Dense(4, activation='softmax')(x)

model = models.Model(inputs, outputs)

# =============================
# COMPILE (SAFE LEARNING RATE)
# =============================
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# =============================
# CALLBACKS (PREVENT OVERFITTING)
# =============================
callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor='val_accuracy',
        patience=3,
        restore_best_weights=True
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=2
    )
]

# =============================
# TRAINING PHASE 1
# =============================
history = model.fit(
    train_data,
    validation_data=test_data,
    epochs=10,
    class_weight=class_weights,
    callbacks=callbacks
)

# =============================
# FINE TUNING (VERY IMPORTANT)
# =============================
base_model.trainable = True

# Freeze early layers (stability)
for layer in base_model.layers[:140]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Continue training
history_finetune = model.fit(
    train_data,
    validation_data=test_data,
    epochs=5,
    class_weight=class_weights,
    callbacks=callbacks
)

# =============================
# SAVE MODEL SAFELY
# =============================
os.makedirs("model", exist_ok=True)
model.save("model/brain_tumor_model.h5")

print("✅ FINAL MODEL TRAINED AND SAVED SUCCESSFULLY")