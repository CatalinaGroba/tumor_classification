#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tensorflow.keras.utils import to_categorical
from tqdm import tqdm
import numpy as np
import os
from PIL import Image


# In[3]:


def load_tumor_images():
    path= ".\\raw_data\Brain-Tumor-Classification-DataSet-master\Brain-Tumor-Classification-DataSet-master.zip\Brain-Tumor-Classification-DataSet-master"
    # Abs -> ~/code/CatalinaGroba/tumor_classification/...
    # Relative -> ./
    
    classes = {'glioma_tumor':0,'meningioma_tumor':1,'pituitary_tumor':2,'no_tumor':3}
    imgs = []
    labels = []
    images = []
    for (name, index) in classes.items():
        curr_images = [elt for elt in os.listdir(os.path.join(path, name))] # This gets all images' names from all different folders

        for img_name in tqdm(curr_images): # Iterate over all names from curr_images
            path = os.path.join(path, name, img_name) # Get the path for every specific image
            if os.path.exists(path): # If correct path
                image = Image.open(path)
                image = image.resize((256, 256))
                images.append(np.array(image)) # Open, resize and append as array to images
                labels.append(index)
            path= "./raw_data/Training"

    X = np.array(images)
    num_classes = len(set(labels))
    y = to_categorical(labels, num_classes)

    # Finally we shuffle:
    p = np.random.permutation(len(X))
    X, y = X[p], y[p]

    first_split = int(len(images) /6.)
    second_split = first_split + int(len(images) * 0.2)
    X_test, X_val, X_train = X[:first_split], X[first_split:second_split], X[second_split:]
    y_test, y_val, y_train = y[:first_split], y[first_split:second_split], y[second_split:]
    
    return X_train, y_train, X_val, y_val, X_test, y_test, num_classes

X_train, y_train, X_val, y_val, X_test, y_test, num_classes = load_tumor_images()


# In[ ]:


from tensorflow.keras.applications import EfficientNetB0

def load_model():
    
    model = EfficientNetB0(weights='imagenet',include_top=False,input_shape=X_train[0].shape)
    
    return model


# In[ ]:


model = load_model()
model.summary()


# In[ ]:


model.compile(loss='categorical_crossentropy',optimizer = 'Adam', metrics= ['accuracy'])


# In[ ]:


def set_nontrainable_layers(model):
    
    model.trainable = False
    
    return model


# In[ ]:


model = set_nontrainable_layers(model)
model.summary()


# In[ ]:


from tensorflow.keras import layers, models

def add_last_layers(model):
    '''Take a pre-trained model, set its parameters as non-trainable, and add additional trainable layers on top'''
    # $CHALLENGIFY_BEGIN
    base_model = set_nontrainable_layers(model)
    flatten_layer = layers.Flatten()
    dense_layer = layers.Dense(500, activation='relu')
    prediction_layer = layers.Dense(3, activation='softmax')
    
    
    model = models.Sequential([
        base_model,
        flatten_layer,
        dense_layer,
        prediction_layer
    ])
    # $CHALLENGIFY_END
    return model


# In[ ]:


model = add_last_layers(model)
model.summary()


# In[ ]:


from tensorflow.keras import optimizers

def build_model():
    # $CHALLENGIFY_BEGIN    
    model = load_model()
    model = add_last_layers(model)
    
    opt = optimizers.Adam(learning_rate=1e-4)
    model.compile(loss='categorical_crossentropy',
                  optimizer=opt,
                  metrics=['accuracy'])
    return model


# In[ ]:


model = build_model()
model.summary()


# In[ ]:


from tensorflow.keras.callbacks import EarlyStopping

model = build_model()

es = EarlyStopping(monitor = 'val_accuracy', 
                   mode = 'max', 
                   patience = 5, 
                   verbose = 1, 
                   restore_best_weights = True)

history = model.fit(X_train, y_train, 
                    validation_data=(X_val, y_val), 
                    epochs=50, 
                    batch_size=16, 
                    callbacks=[es])


# In[ ]:


evaluation = model.evaluate(X_test, y_test)

test_accuracy_vgg = evaluation[-1]


print(f"test_accuracy_vgg = {round(test_accuracy_vgg,2)*100} %")

print(f"test_accuracy = {round(test_accuracy,2)*100} %")

print(f'Chance level: {1./num_classes*100:.1f}%')

