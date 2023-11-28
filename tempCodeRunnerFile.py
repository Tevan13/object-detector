fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Plot the Original Image
    axes[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    axes[0].set_title('Original Image')

    # Plot the Detected Object Image
    axes[1].imshow(cv2.cvtColor(img_contour, cv2.COLOR_BGR2RGB))
    axes[1].set_title('Detected Object')

    # Add text to the PDF
    ax