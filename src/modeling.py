import matplotlib.pyplot as plt
def get_history_graph(history):
    hist_cnn = history.history
    
    loss_values = hist_cnn['loss']
    val_loss_values = hist_cnn['val_loss']
    
    acc_values = hist_cnn['acc'] 
    val_acc_values = hist_cnn['val_acc']
    
    prec_values = hist_cnn['prec'] 
    val_prec_values = hist_cnn['val_prec']

    epochs = range(1, len(loss_values) + 1)

    fig, (ax1, ax2, ax3) = plt.subplots(1,3 , figsize = (15,4))
#     plt.figure(figsize=(15,4))
     
    ax1.plot(epochs, loss_values, 'g.', label='Training loss')
    ax1.plot(epochs, val_loss_values, 'g', label='Validation loss')
    ax1.set_title('Training and validation loss')
    ax1.set_xlabel('Epochs')
    ax1.set_ylabel('Loss')
    ax1.legend()
    
    ax2.plot(epochs, acc_values, 'r.', label='Training acc')
    ax2.plot(epochs, val_acc_values, 'r', label='Validation acc')
    ax2.set_title('Training and validation accuracy')
    ax2.set_xlabel('Epochs')
    ax2.set_ylabel('Accuracy')
    ax2.legend()
    
    ax3.plot(epochs, prec_values, 'b.', label='Training precision')
    ax3.plot(epochs, val_prec_values, 'b', label='Validation precision')
    ax3.set_title('Training and validation precision')
    ax3.set_xlabel('Epochs')
    ax3.set_ylabel('Precision')
    ax3.legend()
    return fig
    
    
    
from keras.metrics import Precision, Recall
from keras.optimizers import Adam
def custom_compile(model):
    adam = Adam(learning_rate = 0.00001)
    
    model.compile(
        optimizer = 'adam',
        loss = 'binary_crossentropy',
        metrics = ['acc', Precision(name='prec'), Recall(name='recall')]
    )
    return


def custom_fit(model, X_train, y_train, X_test, y_test):
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
    threshold = []
    prec = []
    acc = []
    f1 = []
    rec = []
    y_preds = model.predict(X_test)
    for i in np.arange(0,1,0.01):
        y_preds_temp = [1 if x > i else 0 for x in y_preds]
        threshold.append(i)
        prec.append(precision_score(y_test, y_preds_temp))
        acc.append(accuracy_score(y_test, y_preds_temp))
        rec.append(recall_score(y_test, y_preds_temp))
        f1.append(f1_score(y_test, y_preds_temp))
    fig, ax = plt.subplots()
    sns.lineplot(threshold, acc)
    sns.lineplot(threshold, rec)
    sns.lineplot(threshold, prec)
    sns.lineplot(threshold, f1)
    ax.set_xlabel('Threshold')
    ax.set_title('Model Scores by Threshold for Classification')
    ax.legend(['Accuracy','Recall','Precision','F1 score'])
    return fig

from sklearn.metrics import confusion_matrix
def get_roc(model, X_test, y_test):
    y_preds = model.predict(X_test)
    tpr = []
    fpr = []
    for i in np.arange(0,1,0.01):
        y_preds_temp = [1 if x > i else 0 for x in y_preds]
        tn, fp, fn, tp = confusion_matrix(y_test, y_preds_temp).ravel()
        tpr.append(tp/(tp+fn))
        fpr.append(fp/(fp+tn))
    return (tpr, fpr)

def roc_graph(model_list, X_test, y_test):
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