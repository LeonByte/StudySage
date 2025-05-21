# Overfitting in Machine Learning

Overfitting occurs when a machine learning model performs well on training data but poorly on unseen data or the test set. This happens because the model learns the noise and specific patterns in the training data rather than the underlying relationship.

## Signs of Overfitting

1. **High Training Accuracy, Low Test Accuracy**: A significant gap between training and validation performance is a classic sign of overfitting.
2. **Complex Model**: Models with too many parameters relative to the number of training examples can memorize the training data.
3. **Perfect Training Performance**: If your model achieves 100% accuracy on the training set but performs poorly on new data, it has likely overfit.

## How to Prevent Overfitting

- **Cross-validation**: Validate your model on multiple subsets of your data.
- **Regularization**: L1/L2 regularization penalizes large weights to reduce model complexity.
- **Dropout**: Randomly turns off neurons during training to create redundancy.
- **Early Stopping**: Stop training when validation performance begins to degrade.
- **Data Augmentation**: Artificially increase your training data size by creating modified versions of existing data.
- **Simpler Models**: Sometimes a simpler model with fewer parameters can generalize better.

## Example

When training a neural network to classify images, if you have 10,000 parameters but only 100 training examples, the model can effectively "memorize" the correct answer for each training example rather than learning general features for classification. When presented with new images, this model will likely perform poorly.
EOL