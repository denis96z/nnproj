import os
from glob import glob

import numpy
from keract import get_activations, display_activations
from keras import Sequential
from keras.callbacks import TensorBoard, ModelCheckpoint
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.optimizers import SGD
from keras.utils import plot_model
from keras_preprocessing.image import ImageDataGenerator, load_img
from sklearn.metrics import classification_report
from tensorflow.python import confusion_matrix

from const import CHECK_DIR, KERACT_DIR, TF_LOG_DIR, MODEL_DIR, \
    CHAR_IMG_HEIGHT, CHAR_IMG_WIDTH, NUM_ALPHANUM_CHARS, DATA_DIR, ALPHANUM
from utils import create_dir, create_clean_dir, relative_path

TEST_IDX = 2

TF_LOG_PATH = os.path.join(TF_LOG_DIR, 'alphanum', str(TEST_IDX))
KERACT_PATH = os.path.join(KERACT_DIR, 'alphanum', str(TEST_IDX))

MODEL_PATH = os.path.join(MODEL_DIR, 'alphanum')
MODEL_IMG_PATH = os.path.join(MODEL_PATH, f'model_{TEST_IDX:3}.png')
MODEL_STRUCT_PATH = os.path.join(MODEL_PATH, f'model_{TEST_IDX:3}.h5')

DATA_PATH = os.path.join(DATA_DIR, 'alphanum')

TEST_DATA_PATH = os.path.join(DATA_PATH, 'test')
TRAIN_DATA_PATH = os.path.join(DATA_PATH, 'train')

create_clean_dir(TF_LOG_PATH)
create_clean_dir(KERACT_PATH)

create_dir(MODEL_PATH)

model = Sequential()
model.add(Conv2D(filters=12, kernel_size=(3, 3), strides=(1, 1),
                 padding='valid', input_shape=(CHAR_IMG_HEIGHT, CHAR_IMG_WIDTH, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2), padding='valid'))
model.add(Flatten())
model.add(Dense(512, activation='sigmoid'))
model.add(Dense(256, activation='sigmoid'))
model.add(Dense(NUM_ALPHANUM_CHARS, activation='softmax'))
model.compile(optimizer=SGD(lr=0.05), loss='categorical_crossentropy', metrics=['accuracy'])

print('MODEL IS COMPILED')

model.summary()
plot_model(model, to_file=MODEL_IMG_PATH,
           show_shapes=True, show_layer_names=True,
           rankdir='TB', expand_nested=True, dpi=96)

tr_data_gen = ImageDataGenerator(rescale=(1. / 255),
                                 shear_range=0.2,
                                 zoom_range=0.2,
                                 horizontal_flip=True)
train_generator = tr_data_gen.flow_from_directory(TRAIN_DATA_PATH,
                                                  target_size=(CHAR_IMG_HEIGHT, CHAR_IMG_WIDTH),
                                                  color_mode='rgb',
                                                  batch_size=8,
                                                  class_mode='categorical')

print('TRAINING DATASET IS PREPARED')

ts_data_gen = ImageDataGenerator(rescale=(1. / 255))
test_generator = ts_data_gen.flow_from_directory(TEST_DATA_PATH,
                                                 target_size=(CHAR_IMG_HEIGHT, CHAR_IMG_WIDTH),
                                                 color_mode='rgb',
                                                 batch_size=1,
                                                 class_mode='categorical')

print('TESTING DATASET IS PREPARED')

tb_callback = TensorBoard(log_dir=TF_LOG_PATH, histogram_freq=0,
                          write_graph=True, write_images=True)

cp_callback = ModelCheckpoint(monitor='val_accuracy', save_best_only=True,
                              filepath=os.path.join(CHECK_DIR, 'model_{epoch:02d}_{val_accuracy:.3f}.h5'))

model.fit_generator(train_generator,
                    epochs=32, steps_per_epoch=1024,
                    validation_data=test_generator, validation_steps=64,
                    callbacks=[tb_callback, cp_callback])

print('TRAINING COMPLETE')
model.save(MODEL_STRUCT_PATH)

for fp in glob(os.path.join(TEST_DATA_PATH, '*', '7000.png')):
    print(fp)
    (fn, _) = os.path.splitext(fp)
    arr = numpy.array(load_img(fp, target_size=(CHAR_IMG_HEIGHT, CHAR_IMG_WIDTH),
                               grayscale=False, color_mode='rgb', interpolation='nearest'))
    a = get_activations(model, [[arr]], auto_compile=True)
    rp = os.path.join(KERACT_PATH, relative_path(fn, TEST_DATA_PATH))
    display_activations(a, directory=rp, save=True)
    print(f'VISUALIZATION SAVED: {rp}')

print('DONE')


yp = model.predict_generator(test_generator)
yp = numpy.argmax(yp, axis=1)

print('CONFUSION MATRIX:')
print(confusion_matrix(test_generator.classes, yp))
print('Classification Report')
print(classification_report(test_generator.classes, yp, labels=ALPHANUM, target_names=ALPHANUM))
