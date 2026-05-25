import numpy as np
import tensorflow as tf
import cv2

# -----------------------------
# 🔥 GRAD-CAM FUNCTION
# -----------------------------
def get_gradcam(model, img_array, layer_name="last_conv"):
    try:
        # Create model that gives:
        # 1. Output of last conv layer
        # 2. Final prediction
        grad_model = tf.keras.models.Model(
            inputs=model.input,
            outputs=[
                model.get_layer(layer_name).output,
                model.output
            ]
        )

        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(img_array)

            # Get predicted class
            class_idx = tf.argmax(predictions[0])
            loss = predictions[:, class_idx]

        # Compute gradients
        grads = tape.gradient(loss, conv_outputs)

        # If gradients fail
        if grads is None:
            return None

        # Pool gradients
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

        # Weight feature maps
        conv_outputs = conv_outputs[0]

        heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)

        # Normalize heatmap
        heatmap = np.maximum(heatmap, 0)
        heatmap = heatmap / (np.max(heatmap) + 1e-8)

        return heatmap

    except Exception as e:
        print("Grad-CAM error:", e)
        return None


# -----------------------------
# 🔥 OVERLAY HEATMAP ON IMAGE
# -----------------------------
def overlay_heatmap(img, heatmap, alpha=0.4):
    try:
        # Resize heatmap to image size
        heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))

        # Convert to color map
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        # Blend images
        overlay = cv2.addWeighted(img, 1 - alpha, heatmap, alpha, 0)

        return overlay

    except Exception as e:
        print("Overlay error:", e)
        return img