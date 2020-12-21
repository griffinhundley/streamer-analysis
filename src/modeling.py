import matplotlib.pyplot as plt
def get_history_graph(history):
    '''
    Receives 1 parameter, a keras fitted model object.  Returns a figure with diagnostic plots showing the training and validation metrics per epoch.
    '''
    # Get the history object from the model
    hist_cnn = history.history
    
    # Get the list of metrics
    loss_values = hist_cnn['loss']
    val_loss_values = hist_cnn['val_loss']
    
    acc_values = hist_cnn['acc'] 
    val_acc_values = hist_cnn['val_acc']
    
    prec_values = hist_cnn['prec'] 
    val_prec_values = hist_cnn['val_prec']
    
    # Gets the number of epochs
    epochs = range(1, len(loss_values) + 1)

    # Define a figure
    fig, (ax1, ax2, ax3) = plt.subplots(1,3 , figsize = (15,4))
    
    # Plot 1, Loss
    ax1.plot(epochs, loss_values, 'g.', label='Training loss')
    ax1.plot(epochs, val_loss_values, 'g', label='Validation loss')
    ax1.set_title('Training and validation loss')
    ax1.set_xlabel('Epochs')
    ax1.set_ylabel('Loss')
    ax1.legend()
    
    # Plot 2, Accuracy
    ax2.plot(epochs, acc_values, 'r.', label='Training acc')
    ax2.plot(epochs, val_acc_values, 'r', label='Validation acc')
    ax2.set_title('Training and validation accuracy')
    ax2.set_xlabel('Epochs')
    ax2.set_ylabel('Accuracy')
    ax2.legend()
    
    # Plot 3, Precision
    ax3.plot(epochs, prec_values, 'b.', label='Training precision')
    ax3.plot(epochs, val_prec_values, 'b', label='Validation precision')
    ax3.set_title('Training and validation precision')
    ax3.set_xlabel('Epochs')
    ax3.set_ylabel('Precision')
    ax3.legend()
    
    # Return figure
    return fig
    
    
    
from keras.metrics import Precision, Recall
from keras.optimizers import Adam
def custom_compile(model):
    '''
    Receives a keras model object and compiles with preset attributes.  Adam optimizer with 1e-5 learning rate, binary crossentropy loss function, with metrics [loss, accuracy, and precision].
    '''
    # Instantiate the optimizer with the learning rate
    adam = Adam(learning_rate = 0.00001)
    # Compile the model
    model.compile(
        optimizer = 'adam',
        loss = 'binary_crossentropy',
        metrics = ['acc', Precision(name='prec'), Recall(name='recall')]
    )
    return


def custom_fit(model, X_train, y_train, X_test, y_test):
    '''
    Receives a keras model object and train test split data (model, X_train, y_train, X_test, y_test).
    Returns a fitted model with 100 epochs and batch size of 32.
    '''
    # Fit the model to training data.
    history = model.fit(
        X_train,
        y_train, 
        epochs=100,
        batch_size = 32,
        validation_data = (X_test,y_test)
    )
    return history

import seaborn as sns
import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
sns.set_style('darkgrid')
def get_score_graph(model, X_test, y_test):
    '''
    Compares the metrics of a model as a function of its classification threshold and plots the figure.
    (model, X_test, y_test)
    '''
    # Instantiate empty lists
    threshold = []
    prec = []
    acc = []
    f1 = []
    rec = []
    # Generate list of predictions
    y_preds = model.predict(X_test)
    # Calculate metrics for each threshold
    for i in np.arange(0,1,0.01):
        y_preds_temp = [1 if x > i else 0 for x in y_preds]
        threshold.append(i)
        prec.append(precision_score(y_test, y_preds_temp))
        acc.append(accuracy_score(y_test, y_preds_temp))
        rec.append(recall_score(y_test, y_preds_temp))
        f1.append(f1_score(y_test, y_preds_temp))
    # Plot figure with each metric
    fig, ax = plt.subplots()
    sns.lineplot(threshold, acc)
    sns.lineplot(threshold, rec)
    sns.lineplot(threshold, prec)
    sns.lineplot(threshold, f1)
    ax.set_xlabel('Threshold')
    ax.set_title('Model Scores by Threshold for Classification')
    ax.legend(['Accuracy','Recall','Precision','F1 score'])
    # Return the figure
    return fig

from sklearn.metrics import confusion_matrix
def get_roc(model, X_test, y_test):
    '''
    (model, X_test, y_test) takes a model object and X_test, y_test dataframes to calculate the true positive rate and the false positive rate from the confusion matrix at each threshold from 0 to 1.
    '''
    # Generate list of predictions from the test set.
    y_preds = model.predict(X_test)
    tpr = []
    fpr = []
    # For each threshold 0-1, generate a confusion matrix and calculate the TPR and FPR 
    for i in np.arange(0,1,0.01):
        y_preds_temp = [1 if x > i else 0 for x in y_preds]
        tn, fp, fn, tp = confusion_matrix(y_test, y_preds_temp).ravel()
        tpr.append(tp/(tp+fn))
        fpr.append(fp/(fp+tn))
    # Return the TPR and FPR
    return (tpr, fpr)


def roc_graph(model_list, X_test, y_test):
    '''
    This function compares the Receiver Operator Characteristic curve of a list of models by plotting their True Positive Rate as a function of their False Positive Rate.
    (model_list, X_test, y_test)
    '''
    # ROC plot
    fig, ax = plt.subplots(figsize = (12,8))
    ax.set_xlabel('False Positive Rate', fontsize = 12)
    ax.set_ylabel('True Positive Rate', fontsize = 12)
    ax.set_title('ROC', fontsize = 16)
    sns.lineplot([0,1], [0,1], style = True, dashes = [(2,2)], color = 'r', label = 'No Skill')
    legends = ['No_Skill']

    i = 1
    for model in model_list:
        tpr, fpr = get_roc(model, X_test, y_test)
        sns.lineplot(fpr, tpr, label = f'Model {i}')
        i+=1
    ax.legend();
    return fig