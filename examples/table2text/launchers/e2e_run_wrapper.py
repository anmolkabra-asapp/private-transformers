import os

import fire


def _get_cmd(
    output_dir="/mnt/disks/disk-2/dump/privlm2/gpt2_prompt",
    model_name_or_path="distilgpt2",
    ghost_clipping="no",
    max_seq_len=100,
    target_epsilon=8,
    target_delta=1e-5,
    learning_rate=5e-4,
    non_private="no",
    num_train_epochs=10,
    eval_epochs=2,
    store_grads='no',
    orthogonal_projection_path=None,
    orthogonal_projection_rank=None,
):
    task_mode = "e2e"
    data_dir = "/home/lxuechen_stanford_edu/data/prefix-tuning/data/e2e_data"

    cmd = f'''python -m table2text.run_language_modeling \
  --output_dir {output_dir} --overwrite_output_dir \
  --task_mode {task_mode} \
  --model_name_or_path {model_name_or_path} \
  --tokenizer_name {model_name_or_path} \
  --do_train --do_eval \
  --line_by_line \
  --save_steps 100 --save_total_limit 1 --save_at_last no \
  --logging_dir {output_dir} --logging_steps -1 \
  --seed 0 \
  --eval_epochs {eval_epochs} --max_eval_batches 10 --evaluation_strategy epoch --evaluate_before_training "no" --evaluate_during_training "yes" --per_device_eval_batch_size 10 \
  --max_generations 10 --max_generations_train 10 --max_generations_valid 10 \
  --max_train_examples 9223372036854775807 --max_valid_examples 9223372036854775807 --max_eval_examples 9223372036854775807 \
  --data_folder {data_dir} --max_seq_len {max_seq_len} --format_mode cat \
  --per_example_max_grad_norm 0.1 --target_delta {target_delta} --target_epsilon {target_epsilon} \
  --learning_rate {learning_rate} --lr_decay "no" --num_train_epochs {num_train_epochs} --per_device_train_batch_size 16 --gradient_accumulation_steps 64 \
  --non_private {non_private} \
  --ghost_clipping {ghost_clipping} \
  --attention_only "yes" \
  --store_grads {store_grads}'''
    if orthogonal_projection_path is not None:
        cmd += f' --orthogonal_projection_path {orthogonal_projection_path}'
        cmd += f' --orthogonal_projection_rank {orthogonal_projection_rank}'
    return cmd


def main(**kwargs):
    command = _get_cmd(**kwargs)
    print('Running command:')
    print(command)
    os.system(command)


if __name__ == "__main__":
    # python -m table2text.launchers.e2e_run_wrapper
    fire.Fire(main)