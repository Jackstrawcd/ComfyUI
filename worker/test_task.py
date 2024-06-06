#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/6 10:13 AM
# @Author  : wangdongming
# @Site    : 
# @File    : test_task.py
# @Software: xingzhe.ai

txt2img = {
    "client_id": "db20813971164a8d92282b262fdcc543",
    "task_id": "debug_task_1",
    "task_type": 1,
    "prompt": {
        "3": {
            "inputs": {
                "seed": 476173914754017,
                "steps": 20,
                "cfg": 8,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1,
                "model": [
                    "4",
                    0
                ],
                "positive": [
                    "6",
                    0
                ],
                "negative": [
                    "7",
                    0
                ],
                "latent_image": [
                    "5",
                    0
                ]
            },
            "class_type": "KSampler"
        },
        "4": {
            "inputs": {
                "ckpt_name": "flat2DAnimerge_v20.safetensors"
            },
            "class_type": "CheckpointLoaderSimple"
        },
        "5": {
            "inputs": {
                "width": 512,
                "height": 512,
                "batch_size": 1
            },
            "class_type": "EmptyLatentImage"
        },
        "6": {
            "inputs": {
                "text": "beautiful scenery nature glass bottle landscape, , purple galaxy bottle,",
                "clip": [
                    "4",
                    1
                ]
            },
            "class_type": "CLIPTextEncode"
        },
        "7": {
            "inputs": {
                "text": "text, watermark",
                "clip": [
                    "4",
                    1
                ]
            },
            "class_type": "CLIPTextEncode"
        },
        "8": {
            "inputs": {
                "samples": [
                    "3",
                    0
                ],
                "vae": [
                    "4",
                    2
                ]
            },
            "class_type": "VAEDecode"
        },
        "9": {
            "inputs": {
                "filename_prefix": "ComfyUI",
                "images": [
                    "8",
                    0
                ]
            },
            "class_type": "SaveImage"
        }
    }
}

img2img = {
    "client_id": "db20813971164a8d92282b262fdcc543",
    "task_id": "debug-task-2",
    "task_type": 1,
    "prompt": {
        "3": {
            "inputs": {
                "seed": 458931078079564,
                "steps": 20,
                "cfg": 8,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 0.63,
                "model": [
                    "4",
                    0
                ],
                "positive": [
                    "6",
                    0
                ],
                "negative": [
                    "7",
                    0
                ],
                "latent_image": [
                    "14",
                    0
                ]
            },
            "class_type": "KSampler"
        },
        "4": {
            "inputs": {
                "ckpt_name": "flat2DAnimerge_v20.safetensors"
            },
            "class_type": "CheckpointLoaderSimple"
        },
        "6": {
            "inputs": {
                "text": "a beautiful girl",
                "clip": [
                    "4",
                    1
                ]
            },
            "class_type": "CLIPTextEncode"
        },
        "7": {
            "inputs": {
                "text": "text, watermark",
                "clip": [
                    "4",
                    1
                ]
            },
            "class_type": "CLIPTextEncode"
        },
        "8": {
            "inputs": {
                "samples": [
                    "3",
                    0
                ],
                "vae": [
                    "4",
                    2
                ]
            },
            "class_type": "VAEDecode"
        },
        "9": {
            "inputs": {
                "filename_prefix": "ComfyUI",
                "images": [
                    "8",
                    0
                ]
            },
            "class_type": "SaveImage"
        },
        "12": {
            "inputs": {
                "image": "2.jpeg",
                "upload": "image"
            },
            "class_type": "LoadImage"
        },
        "14": {
            "inputs": {
                "pixels": [
                    "12",
                    0
                ],
                "vae": [
                    "4",
                    2
                ]
            },
            "class_type": "VAEEncode"
        }
    },
    "extra_data": {
        "extra_pnginfo": {

        }
    }
}

impaint = {
    "client_id": "db20813971164a8d92282b262fdcc543",
    "task_id": "debug-task-3",
    "task_type": 1,
    "prompt": {
        "3": {
            "inputs": {
                "seed": 496586394045741,
                "steps": 20,
                "cfg": 8,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 0.63,
                "model": [
                    "4",
                    0
                ],
                "positive": [
                    "6",
                    0
                ],
                "negative": [
                    "7",
                    0
                ],
                "latent_image": [
                    "15",
                    0
                ]
            },
            "class_type": "KSampler"
        },
        "4": {
            "inputs": {
                "ckpt_name": "flat2DAnimerge_v20.safetensors"
            },
            "class_type": "CheckpointLoaderSimple"
        },
        "6": {
            "inputs": {
                "text": "beautiful two girls",
                "clip": [
                    "4",
                    1
                ]
            },
            "class_type": "CLIPTextEncode"
        },
        "7": {
            "inputs": {
                "text": "text, watermark",
                "clip": [
                    "4",
                    1
                ]
            },
            "class_type": "CLIPTextEncode"
        },
        "8": {
            "inputs": {
                "samples": [
                    "3",
                    0
                ],
                "vae": [
                    "4",
                    2
                ]
            },
            "class_type": "VAEDecode"
        },
        "9": {
            "inputs": {
                "filename_prefix": "ComfyUI",
                "images": [
                    "8",
                    0
                ]
            },
            "class_type": "SaveImage"
        },
        "12": {
            "inputs": {
                "image": "clipspace/clipspace-mask-1048435.6999999881.png [input]",
                "upload": "image"
            },
            "class_type": "LoadImage"
        },
        "15": {
            "inputs": {
                "grow_mask_by": 6,
                "pixels": [
                    "12",
                    0
                ],
                "vae": [
                    "4",
                    2
                ],
                "mask": [
                    "12",
                    1
                ]
            },
            "class_type": "VAEEncodeForInpaint"
        }
    }
}

TestTasks = [
    txt2img,
    img2img,
    impaint
]
