# -*- coding: utf-8 -*-
"""Final_Code.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VDthLYOFYN6NVfCh_RmltNq3t19wI9lr
"""

!pip install imbalanced-learn # Install the imbalanced-learn library, which includes imblearn

import os
import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import keras
from keras.callbacks import EarlyStopping,ModelCheckpoint
import tensorflow as tf
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from tqdm import tqdm
from imblearn.over_sampling import SMOTE

import os
import cv2
import numpy as np

# Set path to your training dataset
train_dir = '/content/drive/MyDrive/Alzheimer_s Dataset/train'

# Directory to save preprocessed images
preprocessed_dir_train = '/content/drive/MyDrive/Alzheimer_s Dataset/preprocessed_train'

# Create the directory if it does not exist
if not os.path.exists(preprocessed_dir_train):
    os.makedirs(preprocessed_dir_train)

# Function to preprocess an image (crop, resize, normalize)
def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Check if image is loaded properly
    if image is None:
        print(f"Error loading image: {image_path}")
        return None

    # Crop the image to 176x176 (if applicable)
    x, y, w, h = 0, 0, 176, 176  # Modify the crop if necessary
    cropped_image = image[y:y+h, x:x+w]

    # Resize to fixed size 176x176 in case original image dimensions vary
    resized_image = cv2.resize(cropped_image, (176, 176))

    # Normalize the image (scale pixel values to [0, 1])
    normalized_image = resized_image / 255.0

    return normalized_image

# Function to save the preprocessed image
def save_preprocessed_image(image, save_path):
    # Convert the normalized image back to uint8 format (0-255) for saving
    image_to_save = (image * 255).astype(np.uint8)

    # Save the image
    cv2.imwrite(save_path, image_to_save)

# Function to preprocess the entire dataset
def preprocess_dataset(train_dir, preprocessed_dir):
    for class_name in os.listdir(train_dir):
        class_path = os.path.join(train_dir, class_name)

        # Skip if it's not a directory
        if not os.path.isdir(class_path):
            continue

        # Create a directory for the class in the preprocessed directory
        preprocessed_class_dir = os.path.join(preprocessed_dir_train, class_name)
        if not os.path.exists(preprocessed_class_dir):
            os.makedirs(preprocessed_class_dir)

        # Process each image in the class folder
        for image_name in os.listdir(class_path):
            image_path = os.path.join(class_path, image_name)

            # Preprocess the image
            preprocessed_image = preprocess_image(image_path)

            if preprocessed_image is not None:
                # Save the preprocessed image in the new directory
                save_path = os.path.join(preprocessed_class_dir, image_name)
                save_preprocessed_image(preprocessed_image, save_path)
                print(f"Processed and saved: {save_path}")
            else:
                print(f"Skipping image: {image_path}")

# Preprocess the entire training dataset
preprocess_dataset(train_dir, preprocessed_dir_train)

# Function to load an image (original)
def load_image_train(image_path):
    image = cv2.imread(image_path)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

# Function to load a preprocessed image
def load_preprocessed_image_train(image_path):
    image = cv2.imread(image_path)
    return image / 255.0  # Normalize pixel values to [0, 1]
# Function to plot original and preprocessed images
def plot_images(train_dir, preprocessed_dir_train, num_images=10):
    fig, axes = plt.subplots(num_images, 2, figsize=(10, 2 * num_images))
    fig.suptitle("Original vs Preprocessed Images", fontsize=16)

    count = 0
    for class_name in os.listdir(train_dir):
        class_path = os.path.join(train_dir, class_name)

        if not os.path.isdir(class_path):
            continue

        # Load original and preprocessed images
        for image_name in os.listdir(class_path):
            if count >= num_images:
                break

            original_image_path = os.path.join(class_path, image_name)
            preprocessed_image_path = os.path.join(preprocessed_dir_train, class_name, image_name)

            # Load images
            original_image = load_image_train(original_image_path)
            preprocessed_image = load_preprocessed_image_train(preprocessed_image_path)

            # Plot original image
            axes[count, 0].imshow(original_image)
            axes[count, 0].axis('off')
            axes[count, 0].set_title(f"Original: {image_name}")

            # Plot preprocessed image
            axes[count, 1].imshow(preprocessed_image)
            axes[count, 1].axis('off')
            axes[count, 1].set_title(f"Preprocessed: {image_name}")

            count += 1

        if count >= num_images:
            break

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust layout
    plt.show()

# Call the function to plot images
plot_images(train_dir, preprocessed_dir_train, num_images=10)

# Set paths for training data
test_dir = '/content/drive/MyDrive/Alzheimer_s Dataset/test'

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Set path to your test dataset
test_dir = '/content/drive/MyDrive/test'

# Directory to save preprocessed images
preprocessed_dir_test = '/content/drive/MyDrive/Alzheimer_s Dataset/preprocessed_test'

# Create the directory if it does not exist
if not os.path.exists(preprocessed_dir_test):
    os.makedirs(preprocessed_dir_test)

# Function to preprocess an image (crop, resize, normalize)
def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Check if image is loaded properly
    if image is None:
        print(f"Error loading image: {image_path}")
        return None

    # Crop the image to 176x176 (modify the crop if necessary)
    x, y, w, h = 0, 0, 176, 176  # You may need to adjust these values based on the ROI
    cropped_image = image[y:y+h, x:x+w]

    # Resize to fixed size 176x176 in case original image dimensions vary
    resized_image = cv2.resize(cropped_image, (176, 176))

    # Normalize the image (scale pixel values to [0, 1])
    normalized_image = resized_image / 255.0

    return normalized_image

# Function to save the preprocessed image
def save_preprocessed_image(image, save_path):
    # Convert the normalized image back to uint8 format (0-255) for saving
    image_to_save = (image * 255).astype(np.uint8)

    # Save the image
    cv2.imwrite(save_path, image_to_save)

# Function to preprocess the entire dataset
def preprocess_dataset(test_dir, preprocessed_dir_test):
    for class_name in os.listdir(test_dir):
        class_path = os.path.join(test_dir, class_name)

        # Skip if it's not a directory
        if not os.path.isdir(class_path):
            continue

        # Create a directory for the class in the preprocessed directory
        preprocessed_class_dir = os.path.join(preprocessed_dir_test, class_name)
        if not os.path.exists(preprocessed_class_dir):
            os.makedirs(preprocessed_class_dir)

        # Process each image in the class folder
        for image_name in os.listdir(class_path):
            image_path = os.path.join(class_path, image_name)

            # Preprocess the image
            preprocessed_image = preprocess_image(image_path)

            if preprocessed_image is not None:
                # Save the preprocessed image in the new directory
                save_path = os.path.join(preprocessed_class_dir, image_name)
                save_preprocessed_image(preprocessed_image, save_path)
                print(f"Processed and saved: {save_path}")
            else:
                print(f"Skipping image: {image_path}")

# Function to display images
def display_images(image_paths, titles=None):
    plt.figure(figsize=(15, 5))
    for i, image_path in enumerate(image_paths):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB for display
        plt.subplot(2, len(image_paths) // 2, i + 1)
        plt.imshow(image)
        plt.axis('off')
        if titles:
            plt.title(titles[i])
    plt.show()

# Preprocess the entire test dataset
preprocess_dataset(test_dir, preprocessed_dir_test)

# Function to load an image (original)
def load_image_test(image_path):
    try:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error loading image: {image_path}")
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB) if image is not None else None
    except Exception as e:
        print(f"Failed to load image {image_path}: {e}")
        return None

# Function to plot images with additional checks
def plot_images(test_dir, preprocessed_dir_test, num_images=10):
    fig, axes = plt.subplots(num_images, 2, figsize=(10, 2 * num_images))
    fig.suptitle("Original vs Preprocessed Images", fontsize=16)

    count = 0
    for class_name in os.listdir(test_dir):
        class_path = os.path.join(test_dir, class_name)

        if not os.path.isdir(class_path):
            continue

        for image_name in os.listdir(class_path):
            if count >= num_images:
                break

            original_image_path = os.path.join(class_path, image_name)
            preprocessed_image_path = os.path.join(preprocessed_dir_test, class_name, image_name)

            # Load original image
            original_image = load_image_test(original_image_path)

            # Load preprocessed image with checks
            preprocessed_image = load_preprocessed_image_test(preprocessed_image_path)
            if preprocessed_image is None:
                print(f"Skipping preprocessed image: {preprocessed_image_path} - could not load.")
                continue

            # Plot images if both loaded successfully
            if original_image is not None:
                axes[count, 0].imshow(original_image)
                axes[count, 0].axis('off')
                axes[count, 0].set_title(f"Original: {image_name}")

            axes[count, 1].imshow(preprocessed_image)
            axes[count, 1].axis('off')
            axes[count, 1].set_title(f"Preprocessed: {image_name}")

            count += 1

        if count >= num_images:
            break

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust layout
    plt.show()

# Call the function to plot images
plot_images(test_dir, preprocessed_dir_test, num_images=10)



"""## EfficientNetB2 & SMOTE"""

!pip install imbalanced-learn # Install the imbalanced-learn library, which includes imblearn

import os
import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import keras
from keras.callbacks import EarlyStopping,ModelCheckpoint
import tensorflow as tf
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from tqdm import tqdm
from imblearn.over_sampling import SMOTE # Now the import should work

!pip install opendatasets
import opendatasets as od
od.download("https://www.kaggle.com/datasets/tourist55/alzheimers-dataset-4-class-of-images")

train_path = r"/content/alzheimers-dataset-4-class-of-images/Alzheimer_s Dataset/train"
test_path = r"/content/alzheimers-dataset-4-class-of-images/Alzheimer_s Dataset/test"
batch_s = 32
img_size= (224,224)
mode = "rgb"

def df_maker(path):
    file_paths = []
    labels = []

    folds = os.listdir(path)
    for fold in folds:
        fold_path = os.path.join(path,fold)
        file_list = os.listdir(fold_path)
        for file in file_list:
            file_path = os.path.join(fold_path,file)
            file_paths.append(file_path)
            labels.append(fold)


    file_series = pd.Series(file_paths,name="file_paths")
    label_series = pd.Series(labels,name="labels")

    df = pd.concat([file_series,label_series],axis=1)
    return df

train_df = df_maker(train_path)

test_df = df_maker(test_path)

all_data = pd.concat([train_df,test_df])

train_df

test_df

all_data

train_count_df = train_df.labels.value_counts().reset_index()
sns.barplot(data=train_count_df,x="labels",y="count")
plt.title("Number of images of each class for training data")
plt.show()

train_count_df

test_count_df = test_df.labels.value_counts().reset_index()
sns.barplot(data=test_count_df,x="labels",y="count")
plt.title("Number of images of each class for test data")
plt.show()

data_count_df = all_data.labels.value_counts().reset_index()
sns.barplot(data=test_count_df,x="labels",y="count")
plt.title("Number of images of each class for all data")
plt.show()

data_count_df

datagen = tf.keras.preprocessing.image.ImageDataGenerator()

data_generator = datagen.flow_from_dataframe(
    all_data,
    x_col = "file_paths",
    y_col = "labels",
    target_size=img_size,
    batch_size=batch_s,
    color_mode='rgb',
    class_mode='categorical',
    shuffle=False
)

datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

class_dirs = os.listdir(train_path)
plt.figure(figsize=(21, 24))
for i in range(len(class_dirs)):
    plt.subplot(4,2,i+1)
    img_path = f"{train_path}/{class_dirs[i]}/{os.listdir(f'{train_path}/{class_dirs[i]}')[0]}"
    img = plt.imread(img_path)/255
    plt.title(class_dirs[i])
    plt.imshow(img,cmap="gray")

data_imgs=np.concatenate([next(data_generator)[0] for i in range(data_generator.__len__())])
data_labels=np.concatenate([next(data_generator)[1] for i in range(data_generator.__len__())])

data_imgs = data_imgs.reshape(-1, 224*224* 3)
data_imgs,data_labels = SMOTE(random_state=7).fit_resample(data_imgs,data_labels)
data_imgs = data_imgs.reshape(-1,224,224,3)

data_generator.class_indices

map  ={0:'MildDemented',
 1:'ModerateDemented',
 2:'NonDemented',
 3:'VeryMildDemented'}

labels=pd.Series([map[i] for i in np.argmax(data_labels,axis=1)],name="label")
labels_count = labels.value_counts().reset_index()
sns.barplot(data=labels_count,x="label",y="count")
plt.show()

labels_count

train_imgs, test_imgs, train_labels,test_labels = train_test_split(data_imgs,data_labels,  train_size= 0.75, shuffle= True, random_state= 7,stratify=data_labels)

test_imgs, val_imgs, test_labels,val_labels = train_test_split(test_imgs,test_labels,  train_size= 0.5, shuffle= True, random_state= 7,stratify= test_labels)

train_imgs.shape

val_imgs.shape

test_imgs.shape

base_model =tf.keras.applications.EfficientNetB2(include_top=False, weights="imagenet", input_shape=(224,224,3),pooling='max')

from tensorflow.keras.layers import Dense, Dropout # Import Dense and Dropout layers
from tensorflow.keras import regularizers  # Import regularizers
import tensorflow as tf
from tensorflow import keras

x = base_model.output
x = Dense(256, activation="relu", kernel_regularizer=regularizers.l2(0.001))(x)
x = Dropout(0.4)(x)
predictions = Dense(4, activation='softmax')(x)

model = keras.models.Model(inputs=base_model.input, outputs=predictions)

# for layer in base_model.layers:
# layer.trainable= False


model.compile(loss="categorical_crossentropy", optimizer=keras.optimizers.Adamax(learning_rate=0.001),
              metrics=["accuracy", "AUC"])

model.summary()

from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau  # Import ReduceLROnPlateau

checkpoint = ModelCheckpoint('alzheimer\'s_model.keras', monitor='val_accuracy', save_best_only=True, mode='max')
reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.4,
    patience=3,
    min_lr=1e-7,
    verbose=1
)

history = model.fit(
    train_imgs,train_labels,
    epochs = 10,
    validation_data = [val_imgs,val_labels],
    batch_size=batch_s,
    callbacks = [checkpoint,reduce_lr]
)

model.evaluate(test_imgs,test_labels)

train_acc = history.history['accuracy']
train_loss = history.history['loss']
val_acc = history.history['val_accuracy']
val_loss = history.history['val_loss']

epochs = [i+1 for i in range(len(train_acc))]

plt.figure(figsize=(12,9))
plt.subplot(2,1,1)
plt.plot(epochs,train_loss,'b',label="Train Loss")
plt.plot(epochs,val_loss,'g',label="Validation loss")
plt.title("Loss")
plt.legend()
plt.xlabel('Epochs')
plt.ylabel('Loss')

plt.figure(figsize=(12,9))
plt.subplot(2,1,1)
plt.plot(epochs,train_acc,'b',label="Train Accuracy")
plt.plot(epochs,val_acc,'g',label="Validation Accuracy")
plt.title("Accuracy")
plt.legend()
plt.xlabel('Epochs')
plt.ylabel('Accuracy')

plt.tight_layout()
plt.show()

predictions = model.predict(test_imgs)
y_pred = np.argmax(predictions, axis = 1)
y_true = np.argmax(test_labels, axis = 1)

print(classification_report(y_true,y_pred))

cm = confusion_matrix(y_true, y_pred)
sns.heatmap(cm, annot=True,fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Truth')
plt.title("EfficientNetB2 confusion matrix")
plt.show()

model.save('/content/drive/MyDrive/alzheimers_smote.h5')  # Save in HDF5 format



"""### CNN MODEL"""

import os
import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing.image import ImageDataGenerator
import keras
from keras.callbacks import EarlyStopping,ModelCheckpoint
import tensorflow as tf
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from tqdm import tqdm
from imblearn.over_sampling import SMOTE

!pip install opendatasets
import opendatasets as od
od.download("https://www.kaggle.com/datasets/tourist55/alzheimers-dataset-4-class-of-images")

images = []
labels = []
for subfolder in tqdm(os.listdir('/content/alzheimers-dataset-4-class-of-images/Alzheimer_s Dataset')):
    subfolder_path = os.path.join('/content/alzheimers-dataset-4-class-of-images/Alzheimer_s Dataset', subfolder)
    for folder in os.listdir(subfolder_path):
        subfolder_path2=os.path.join(subfolder_path,folder)
        for image_filename in os.listdir(subfolder_path2):
            image_path = os.path.join(subfolder_path2, image_filename)
            images.append(image_path)
            labels.append(folder)
df = pd.DataFrame({'image': images, 'label': labels})
df

plt.figure(figsize=(15,8))
ax = sns.countplot(x=df.label,palette='Set1')
ax.set_xlabel("Class",fontsize=20)
ax.set_ylabel("Count",fontsize=20)
plt.title('The Number Of Samples For Each Class',fontsize=20)
plt.grid(True)
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(50,50))
for n,i in enumerate(np.random.randint(0,len(df),50)):
    plt.subplot(10,5,n+1)
    img=cv2.imread(df.image[i])
    img=cv2.resize(img,(224,224))
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.axis('off')
    plt.title(df.label[i],fontsize=25)

Size=(176,176)
work_dr = ImageDataGenerator(
    rescale = 1./255
)
train_data_gen = work_dr.flow_from_dataframe(df,x_col='image',y_col='label', target_size=Size, batch_size=6500, shuffle=False)

train_data, train_labels = train_data_gen.next()

class_num=np.sort(['MildDemented','ModerateDemented','NonDemented','VeryMildDemented'])
class_num

sm = SMOTE(random_state=42)
train_data, train_labels = sm.fit_resample(train_data.reshape(-1, 176 * 176 * 3), train_labels)
train_data = train_data.reshape(-1, 176,176, 3)
print(train_data.shape, train_labels.shape)

labels=[class_num[i] for i in np.argmax(train_labels,axis=1) ]
plt.figure(figsize=(15,8))
ax = sns.countplot(x=labels,palette='Set1')
ax.set_xlabel("Class",fontsize=20)
ax.set_ylabel("Count",fontsize=20)
plt.title('The Number Of Samples For Each Class',fontsize=20)
plt.grid(True)
plt.xticks(rotation=45)
plt.show()

X_train, X_test1, y_train, y_test1 = train_test_split(train_data,train_labels, test_size=0.3, random_state=42,shuffle=True,stratify=train_labels)
X_val, X_test, y_val, y_test = train_test_split(X_test1,y_test1, test_size=0.5, random_state=42,shuffle=True,stratify=y_test1)
print('X_train shape is ' , X_train.shape)
print('X_test shape is ' , X_test.shape)
print('X_val shape is ' , X_val.shape)
print('y_train shape is ' , y_train.shape)
print('y_test shape is ' , y_test.shape)
print('y_val shape is ' , y_val.shape)

model=keras.models.Sequential()
model.add(keras.layers.Conv2D(32,kernel_size=(3,3),strides=2,padding='same',activation='relu',input_shape=(176,176,3)))
model.add(keras.layers.MaxPool2D(pool_size=(2,2),strides=2,padding='same'))
model.add(keras.layers.Conv2D(64,kernel_size=(3,3),strides=2,activation='relu',padding='same'))
model.add(keras.layers.MaxPool2D((2,2),2,padding='same'))
model.add(keras.layers.Conv2D(128,kernel_size=(3,3),strides=2,activation='relu',padding='same'))
model.add(keras.layers.MaxPool2D((2,2),2,padding='same'))
model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(1024,activation='relu'))
model.add(keras.layers.Dropout(0.3))
model.add(keras.layers.Dense(4,activation='softmax'))
model.summary()

tf.keras.utils.plot_model(model, to_file='model.png', show_shapes=True, show_layer_names=True,show_dtype=True,dpi=120)

checkpoint_cb =ModelCheckpoint("CNN_model.h5", save_best_only=True)
early_stopping_cb =EarlyStopping(patience=10, restore_best_weights=True)
model.compile(optimizer ='adam', loss='categorical_crossentropy', metrics=['accuracy'])
hist = model.fit(X_train,y_train, epochs=50, validation_data=(X_val,y_val), callbacks=[checkpoint_cb, early_stopping_cb])

hist_=pd.DataFrame(hist.history)
hist_

plt.figure(figsize=(15,10))
plt.subplot(1,2,1)
plt.plot(hist_['loss'],label='Train_Loss')
plt.plot(hist_['val_loss'],label='Validation_Loss')
plt.title('Train_Loss & Validation_Loss',fontsize=20)
plt.legend()
plt.subplot(1,2,2)
plt.plot(hist_['accuracy'],label='Train_Accuracy')
plt.plot(hist_['val_accuracy'],label='Validation_Accuracy')
plt.title('Train_Accuracy & Validation_Accuracy',fontsize=20)
plt.legend()
plt.show()

score, acc= model.evaluate(X_test,y_test)
print('Test Loss =', score)
print('Test Accuracy =', acc)

predictions = model.predict(X_test)
y_pred = np.argmax(predictions,axis=1)
y_test_ = np.argmax(y_test,axis=1)
df = pd.DataFrame({'Actual': y_test_, 'Prediction': y_pred})
df

plt.figure(figsize=(50,50))
for n,i in enumerate(np.random.randint(0,len(X_test),20)):
    plt.subplot(10,2,n+1)
    plt.imshow(X_test[i])
    plt.axis('off')
    plt.title(f'{class_num[y_test_[i]]} ==== {class_num[y_pred[i]]}',fontsize=27)

ClassificationReport = classification_report(y_test_,y_pred)
print('Classification Report is : ', ClassificationReport )

CM = confusion_matrix(y_test_,y_pred)
CM_percent = CM.astype('float') / CM.sum(axis=1)[:, np.newaxis]
sns.heatmap(CM_percent,fmt='g',center = True,cbar=False,annot=True,cmap='Blues')
CM

model.save("my model.h5")

# prompt: save this as hdf5 file

model.save('/content/drive/MyDrive/my_model.h5')



!pip install imbalanced-learn # Install the imbalanced-learn library, which includes imblearn

!pip install opendatasets
import opendatasets as od
od.download("https://www.kaggle.com/datasets/tourist55/alzheimers-dataset-4-class-of-images")

import os
import cv2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
# from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import keras
from keras.callbacks import EarlyStopping,ModelCheckpoint
import tensorflow as tf
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from tqdm import tqdm
from imblearn.over_sampling import SMOTE

images = []
labels = []
for subfolder in tqdm(os.listdir('/content/alzheimers-dataset-4-class-of-images/Alzheimer_s Dataset')):
    subfolder_path = os.path.join('/content/alzheimers-dataset-4-class-of-images/Alzheimer_s Dataset', subfolder)
    for folder in os.listdir(subfolder_path):
        subfolder_path2=os.path.join(subfolder_path,folder)
        for image_filename in os.listdir(subfolder_path2):
            image_path = os.path.join(subfolder_path2, image_filename)
            images.append(image_path)
            labels.append(folder)
df = pd.DataFrame({'image': images, 'label': labels})
df

plt.figure(figsize=(15,8))
ax = sns.countplot(x=df.label,palette='Set1')
ax.set_xlabel("Class",fontsize=20)
ax.set_ylabel("Count",fontsize=20)
plt.title('The Number Of Samples For Each Class',fontsize=20)
plt.grid(True)
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(50,50))
for n,i in enumerate(np.random.randint(0,len(df),50)):
    plt.subplot(10,5,n+1)
    img=cv2.imread(df.image[i])
    img=cv2.resize(img,(224,224))
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.axis('off')
    plt.title(df.label[i],fontsize=25)

Size=(176,176)
work_dr = ImageDataGenerator(
    rescale = 1./255
)
train_data_gen = work_dr.flow_from_dataframe(df,x_col='image',y_col='label', target_size=Size, batch_size=6500, shuffle=False)

for i in range(len(train_data_gen)):
    train_data, train_labels = train_data_gen[i]

class_num=np.sort(['MildDemented','ModerateDemented','NonDemented','VeryMildDemented'])
class_num

sm = SMOTE(random_state=42)
train_data, train_labels = sm.fit_resample(train_data.reshape(-1, 176 * 176 * 3), train_labels)
train_data = train_data.reshape(-1, 176,176, 3)
print(train_data.shape, train_labels.shape)

labels=[class_num[i] for i in np.argmax(train_labels,axis=1) ]
plt.figure(figsize=(15,8))
ax = sns.countplot(x=labels,palette='Set1')
ax.set_xlabel("Class",fontsize=20)
ax.set_ylabel("Count",fontsize=20)
plt.title('The Number Of Samples For Each Class',fontsize=20)
plt.grid(True)
plt.xticks(rotation=45)
plt.show()

X_train, X_test1, y_train, y_test1 = train_test_split(train_data,train_labels, test_size=0.3, random_state=42,shuffle=True,stratify=train_labels)
X_val, X_test, y_val, y_test = train_test_split(X_test1,y_test1, test_size=0.5, random_state=42,shuffle=True,stratify=y_test1)
print('X_train shape is ' , X_train.shape)
print('X_test shape is ' , X_test.shape)
print('X_val shape is ' , X_val.shape)
print('y_train shape is ' , y_train.shape)
print('y_test shape is ' , y_test.shape)
print('y_val shape is ' , y_val.shape)

from tensorflow.keras.applications.vgg19 import VGG19
from tensorflow.keras.layers import Input, Lambda, Dense, Flatten, Dropout
from tensorflow.keras.models import Model
vgg = VGG19(input_shape=(176,176,3), weights='imagenet', include_top=False)
for layer in vgg.layers:
    layer.trainable = False
x = Flatten()(vgg.output)

prediction = Dense(4, activation='softmax')(x)

modelvgg = Model(inputs=vgg.input, outputs=prediction)
modelvgg.summary()

tf.keras.utils.plot_model(modelvgg, to_file='model.png', show_shapes=True, show_layer_names=True,show_dtype=True,dpi=120)

checkpoint_cb =ModelCheckpoint("modelvgg.keras", save_best_only=True)
early_stopping_cb =EarlyStopping(patience=10, restore_best_weights=True)
modelvgg.compile(optimizer ='adam', loss='categorical_crossentropy', metrics=['accuracy'])
hist = modelvgg.fit(X_train,y_train, epochs=100, validation_data=(X_val,y_val), callbacks=[checkpoint_cb, early_stopping_cb])

hist_=pd.DataFrame(hist.history)
hist_

plt.figure(figsize=(15,10))
plt.subplot(1,2,1)
plt.plot(hist_['loss'],label='Train_Loss')
plt.plot(hist_['val_loss'],label='Validation_Loss')
plt.title('Train_Loss & Validation_Loss',fontsize=20)
plt.legend()
plt.subplot(1,2,2)
plt.plot(hist_['accuracy'],label='Train_Accuracy')
plt.plot(hist_['val_accuracy'],label='Validation_Accuracy')
plt.title('Train_Accuracy & Validation_Accuracy',fontsize=20)
plt.legend()
plt.show()

score, acc= modelvgg.evaluate(X_test,y_test)
print('Test Loss =', score)
print('Test Accuracy =', acc)

auc=modelvgg.evaluate(X_test,y_test)
print('AUC =', auc)

CM = confusion_matrix(y_test_,y_pred)
CM_percent = CM.astype('float') / CM.sum(axis=1)[:, np.newaxis]
sns.heatmap(CM_percent,fmt='g',center = True,cbar=False,annot=True,cmap='Blues')
CM

predictions = modelvgg.predict(X_test)
y_pred = np.argmax(predictions,axis=1)
y_test_ = np.argmax(y_test,axis=1)
df = pd.DataFrame({'Actual': y_test_, 'Prediction': y_pred})
df

ClassificationReport = classification_report(y_test_,y_pred)
print('Classification Report is : ', ClassificationReport )

modelvgg.save('modelvgg.h5') # Change 'model' to 'modelvgg' to match your model variable name

import tensorflow as tf

tf.keras.models.save_model(modelvgg, 'modelvgg') # Using tf.keras.models.save_model