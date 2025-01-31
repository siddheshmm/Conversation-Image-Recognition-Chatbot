import torch
from torchvision import models, transforms
from PIL import Image

class ImageRecognizer:
    def __init__(self):
        self.model = models.resnet152(pretrained=True)
        self.model.eval()
        self.labels = self._load_imagenet_labels()
        
        self.preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
    
    def _load_imagenet_labels(self):
        with open('imagenet_classes.txt') as f:
            return [line.strip() for line in f.readlines()]
    
    def predict(self, image_path):
        img = Image.open(image_path)
        img_t = self.preprocess(img)
        batch_t = torch.unsqueeze(img_t, 0)
        
        with torch.no_grad():
            out = self.model(batch_t)
        
        _, index = torch.max(out, 1)
        percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
        return self.labels[index[0]], round(percentage[index[0]].item(), 2)