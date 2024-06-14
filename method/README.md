## Installing Dependencies and Setting Up

```
git clone https://github.com/vlgiitr/unmasking-the-veil.git
cd unmasking-the-veil/method
conda env create -f environment.yaml
conda activate unmasking
cd ..
mkdir assets/pretrained_models
cd assets/pretrained_models
wget https://huggingface.co/CompVis/stable-diffusion-v-1-4-original/resolve/main/sd-v1-4.ckpt
wget https://dl.fbaipublicfiles.com/sscd-copy-detection/sscd_imagenet_mixup.torchscript.pt
cd ../../compvis
```
## Training and Experiments 

All our experiments were conducted on 2 A100 GPUs taking approximately 32GBs of memory however,to run them at lower memory the models can be run at 16 bit precision 

**Style Ablation**

```
python train.py -t --gpus 1,2 --concept_type style --caption_target  "van gogh" --prompts ../assets/finetune_prompts/vangogh.txt --name "vangogh_painting"  --train_size 200
```

**Instance Ablation**

```
python train.py -t --gpus 1,2 --concept_type object --caption_target  "cat+grumpy cat" --prompts ../assets/finetune_prompts/cat.txt --name "grumpy_cat" --train_size 200
```
Where cat is the anchor concept and grumpy cat is the target concept 

**Memorized Image Ablation**

```
python train.py -t --gpus 1,2 --concept_type memorization --caption_target  "Captain Marvel Poster" --prompts ../assets/finetune_prompts/marvel_mem.txt --name "Marvel" --mem_impath ../assets/mem_images/marvel.png  --train_size 400
```

Where marvel.png is the memorized image 

**Trademark Ablation**

```
python train.py -t --gpus 1,2 --concept_type logo --caption_target  "Logo+Starbucks Logo" --prompts ../assets/finetune_prompts/starbucks.txt --name "starbucks" --train_size 400
```

Arguments : 

* `concept_type`: ['style', 'object', 'memorization','logo'] (required)
* `caption_target`: Concept to be removed (artist, e.g., "van gogh" or instance, e.g., "cat+grumpy cat" or memorization prompt, e.g., "New Orleans House Galaxy Case" )
* `prompts`: Path to the prompts used for fine-tuning 
* `name`: Name of the experiment
* `mem_impath`: Path to the memorized image (required when concept_type='memorization')

Optional:

* `parameter_group`: ['full-weight', 'cross-attn', 'embedding'] (default: 'cross-attn')
* `loss_type_reverse`: The loss type for fine-tuning. ['model-based', 'noise-based'] (default: 'model-based')
* `resume-from-checkpoint-custom`: The checkpoint path of pretrained model
* `regularization`: Store-true, add regularization loss
* `train_size`: Number of generated images for fine-tuning (default: 1000)
* `train_max_steps`: Overwrite max_steps in fine-tuning (default: 100 for style and object, 400 for memorization,400 for trademarks)
* `base_lr`: Overwrite base learning rate (default: 2e-6 for style,object and trademark, 5e-7 for memorization)
* `save_freq`: Checkpoint saving steps (default: 100)
* `logdir`: Path where the experiment is saved (default: log_testing)
* `n_samples`:Batch size for image generation 
* `rc`: True if you want to resume from a checkpoint 
* `wandb_entity`: Name of entity(If used) 

**Note:** All results in our work were reported for model-based loss type.

#### Sampling

```
python sample.py --ckpt {} --from-file {} --ddim_steps 100 --outdir {} --n_copies 10 
```

* `ckpt`: The location to checkpoint path(In log_testing for trained model)
* `from-file`: the path to prompts txt file
* `outdir`: the path to image directory
* `name`: the name used for  logging
* `n_copies`: the number of copies for each prompt

#### Evaluation of Ablating Style and Instance

For model evaluation, we provide a script to compute CLIP score, CLIP accuracy and KID metrics.
It consists of two separate stages, **generation** and **evaluation**

**Generation Stage**

```
python evaluate.py --gpu 0,1 --root {} --filter {} --concept_type {} --caption_target {}  --outpkl {} --base_outpath {} --eval_json {}
```

* `root`: the location to root training folder which contains a folder called `checkpoints`
* `filter`: a regular expression to filter the checkpoint to evaluate (default: step_*.ckpt)

* `n_samples`: batch-size for sampling images
* `concept_type`: choose from ['style', 'object', 'memorization']
* `caption_target`: the target for ablated concept
* `outpkl`: the location to save evaluation results (default: metrics/evaluation.pkl)
* `base_outpath`: the path to the root of baseline generation for FID, KID.
* `eval_json`: the path to a formatted json file for evaluation metadata

**Evaluation Stage**

```
python evaluate.py --gpu 0,1 --root {} --filter {} --concept_type {} --caption_target {}  --outpkl {} --base_outpath {} --eval_json {} --eval_stage
```

the same script with additional parameters: `--eval_stage`

**Adding entries to eval_json file**

For customized concepts, a user has to manually specify a **new entry** in eval_json file and put that to the correct concept type.
Hard negative categories are those that are similar to the ablated concept but should be preserved in the fine-tuned model.
Also create a `anchor_concept_eval.txt` file in `../assets/eval_prompts/` with prompts to be used for evaluation for instance ablation. 
In case of style ablation, provide the `<style-name>_eval.txt` with prompts for each of the target and surrounding styles. 

````
caption target:{
	target: caption target 
	anchor: caption anchor
	hard_negatives:[
		caption hard negative 1,
		caption hard negative 2,
		...
		caption hard negative m,
	]
}
````

#### Evaluation of Ablating Memorized Image

```
python sample.py --ckpt {} --prompt "New Orleans House Galaxy Case" --ddim_steps 50 --outdir samples_eval --n_copies 200 
python src/filter.py --folder {} --impath ../assets/mem_images/orleans.png --outpath {}
```
where `folder` is the path to saved images, i.e., `{ckpt-path}/samples_eval/` and outpath is the folder to save the images which are different than the memorized image.

#### Custom Evaluation 

In order to run the Clip Score based evaluation mentioned : [here](https://github.com/Taited/clip-score.git) 
We first need to rename the images sequentially and then further create a prompts directory

**Structure of Directory**

```plaintext
├── path/to/image
│   ├── cat.png
│   ├── dog.png
│   └── bird.jpg
└── path/to/text
    ├── cat.txt
    ├── dog.txt
    └── bird.txt
```

```
python rename.py --prompt_file_path {} --images_folder_path{}
python file.py --prompt_file_path {} --prompts_folder{}
```
To calculate CLIP Score 

```
python -m clip_score path/to/image_folder path/to/text_folder
```
**Note:** The jailbreak prompts we use for evaluation are available [here](assets/jailbreak_prompts)