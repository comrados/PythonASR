import tensorflow as tf
from tensorflow import keras

def mnist_basic():
    fmnist = keras.datasets.fashion_mnist
    mnist = keras.datasets.mnist
    # load and normalize
    (x_train, y_train), (x_test, y_test) = fmnist.load_data()
    x_train, x_test = x_train / 255.0, x_test / 255.0
    # model
    model = tf.keras.models.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(512, activation=tf.nn.relu),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(10, activation=tf.nn.softmax)
    ])
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    # train & eval
    model.fit(x_train, y_train, epochs=5)
    model.evaluate(x_test, y_test)


mnist_basic()
