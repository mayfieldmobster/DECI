import os
import json

import tensorflow as tf
import model

def run(batch_size):
    per_worker_batch_size = batch_size
    tf_config = json.loads(os.environ['TF_CONFIG'])
    num_workers = len(tf_config['cluster']['worker'])

    strategy = tf.distribute.MultiWorkerMirroredStrategy()

    global_batch_size = per_worker_batch_size * num_workers
    multi_worker_dataset = model.dataset(global_batch_size)

    with strategy.scope():
        # Model building/compiling need to be within `strategy.scope()`.
        multi_worker_model = model.build_and_compile_cnn_model()


    multi_worker_model.fit(multi_worker_dataset, epochs=3, steps_per_epoch=70)