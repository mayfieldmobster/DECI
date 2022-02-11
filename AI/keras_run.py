import tensorflow as tf
import horovod.keras as hvd
import model
import keras


def run(batch_size, epochs, sharding_type="OFF",
        shuffle=True, class_weight=None, sample_weight=None,
        initial_epoch=0, steps_per_epoch=None, max_queue_size=10, compression=None):

    # Horovod: initialize Horovod.
    hvd.init()

    # Horovod: pin GPU to be used to process local rank (one GPU per process)
    gpus = tf.config.experimental.list_physical_devices('GPU')
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
    if gpus:
        tf.config.experimental.set_visible_devices(gpus[hvd.local_rank()], 'GPU')

    data = model.dataset()
    complete_model = model.model()
    loss = model.loss()
    opt = model.opt()

    opt = hvd.DistributedOptimizer(opt)

    complete_model.compile(loss=loss,
                           optimizer=opt,
                           metrics=["accuracy"]
                           )

    callbacks = [
        # Horovod: broadcast initial variable states from rank 0 to all other processes.
        # This is necessary to ensure consistent initialization of all workers when
        # training is started with random weights or restored from a checkpoint.
        hvd.callbacks.BroadcastGlobalVariablesCallback(0),
    ]

    if hvd.rank() == 0:
        callbacks.append(keras.callbacks.ModelCheckpoint('./checkpoint-{epoch}.h5'))

    complete_model.fit(data, epochs=epochs, verbose=0,
                       shuffle=shuffle, class_weight=class_weight,
                       sample_weight=sample_weight, initial_epoch=initial_epoch,
                       steps_per_epoch=steps_per_epoch,max_queue_size=max_queue_size,
                      )# custom training loop
