import matplotlib.pyplot as plt
def get_history_graph(history):
    hist_cnn = history.history
    loss_values = hist_cnn['loss']
    val_loss_values = hist_cnn['val_loss']
    acc_values = hist_cnn['acc'] 
    val_acc_values = hist_cnn['val_acc']


    epochs = range(1, len(loss_values) + 1)

    plt.figure(figsize=(15,4))
    plt.subplot(121)
    plt.plot(epochs, loss_values, 'g.', label='Training loss')
    plt.plot(epochs, val_loss_values, 'g', label='Validation loss')

    plt.title('Training and validation loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    plt.subplot(122)
    plt.plot(epochs, acc_values, 'r.', label='Training acc')
    plt.plot(epochs, val_acc_values, 'r', label='Validation acc')
    plt.title('Training and validation accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()
    
from keras.metrics import Precision, Recall
from keras.optimizers import Adam
def custom_compile(model):
    adam = Adam(learning_rate = 0.00001)
    model.compile(
        optimizer = 'adam',
        loss = 'binary_crossentropy',
        metrics = ['acc', Precision(), Recall()]
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
    return