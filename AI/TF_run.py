import os
import json
import tensorflow as tf
import model


def run(batch_size, epochs, sharding_type="OFF",
                           shuffle=True,
                           class_weight=None, sample_weight=None, initial_epoch=0, steps_per_epoch=None,
                           max_queue_size=10):

    per_worker_batch_size = batch_size
    tf_config = json.loads(os.environ['TF_CONFIG'])
    num_workers = len(tf_config['cluster']['worker'])

    strategy = tf.distribute.MultiWorkerMirroredStrategy()

    global_batch_size = per_worker_batch_size * num_workers
    dataset = model.dataset(global_batch_size)

    if sharding_type == "OFF":
        options = tf.data.Options()
        options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.OFF
        dataset = dataset.with_options(options)

    elif sharding_type == "DATA":
        options = tf.data.Options()
        options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.DATA
        dataset = dataset.with_options(options)

    elif sharding_type == "AUTO":
        options = tf.data.Options()
        options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.AUTO
        dataset = dataset.with_options(options)

    elif sharding_type == "FILE":
        options = tf.data.Options()
        options.experimental_distribute.auto_shard_policy = tf.data.experimental.AutoShardPolicy.FILE
        dataset = dataset.with_options(options)

    with strategy.scope():
        # Model building/compiling need to be within `strategy.scope()`.
        multi_worker_model = model.build_and_compile_model()

    multi_worker_model.fit(dataset, epochs=epochs, verbose=0,
                           shuffle=shuffle, class_weight=class_weight,
                           sample_weight=sample_weight, initial_epoch=initial_epoch, steps_per_epoch=steps_per_epoch,
                           max_queue_size=max_queue_size,
                           )
