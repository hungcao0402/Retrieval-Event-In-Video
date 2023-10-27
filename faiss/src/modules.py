import faiss
import numpy as np
import clip
from typing import List, Optional
import torch
from lavis.models import load_model_and_preprocess


class Faiss: 
    def __init__(self, database_path: str, use_gpu: bool = True) -> None:
        database = np.load(database_path)
        
        db_size, dim = database.shape
        print('Indexing database...')
        print('database shape:', database.shape)
        self.index_flat = self._get_indexer(dim, 'IP')

        if use_gpu:
            res = faiss.StandardGpuResources()  # use a single GPU

            # make it into a gpu index
            self.index_flat = faiss.index_cpu_to_gpu(res, 0, self.index_flat)

        self.index_flat.add(database)


        print('Finish indexing database')
        
    def _get_indexer(self, dim: int, id_type: str):
        if id_type == 'L2':
            return faiss.IndexFlatL2(dim)
        return faiss.IndexFlatIP(dim)
    
    def search(self, encoded_queries: np.array, top_k: int) -> np.array:
        """_Return indexes of every query in queries

        Args:
            queries (np.array): (n_queries, dim)
            top_k (int): top k nearest

        Returns:
            np.array: (n_queries, top_k)
        """
        print('query.shape:', encoded_queries.shape)
        
        distances, indices = self.index_flat.search(encoded_queries, top_k)
        return distances, indices
    


class Encoder:
    def __init__(self, model_name: str='ViT-B/16',project=None, use_gpu: bool = True) -> None:
        if use_gpu:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = 'cpu'
        self.model_name = model_name
        self.project = project
        print('Loading model...')
        if self.model_name == 'BLIP':
            self.model, self.preprocess, self.tokenize = load_model_and_preprocess(
                                                        name="blip2_feature_extractor",
                                                        model_type="pretrain",
                                                        is_eval=True,
                                                        device=self.device)
        else:
            self.tokenize = clip.tokenize
            self.model, self.preprocess = clip.load(model_name, device=self.device)

        print('Finish loading model.')
            
    def encode_texts(self, text: List[str]) -> np.array:
        if self.model_name == 'BLIP':
            text_input = self.tokenize["eval"](text[0])
            sample = {"image": "", "text_input": [text_input]}
            features_text = self.model.extract_features(sample, mode="text")
            if self.project:
                text_features = features_text
            else:
                text_features = features_text
        else:
            tokenized_text = self.tokenize(text).to(self.device)
            with torch.no_grad():
                text_features = self.model.encode_text(tokenized_text)
                text_features = text_features.cpu().numpy()
                text_features = text_features / np.linalg.norm(text_features)
        return text_features
            
    def encode_image(self, image) -> np.array:
        
        if self.model_name == 'BLIP':
            from PIL import Image
            image = Image.fromarray(cv2.imread(img_file))
            image = vis_processors["eval"](image).unsqueeze(0).cuda()
            sample = {"image": image, "text_input": [""]}
            feature_image = model.extract_features(sample, mode="image")
            if self.project:
                text_features = features_text.image_embeds_proj
                print('project=True:', text_features.shape)
            else:
                text_features = features_text.image_embeds
                print('project=False:', text_features.shape)
        else:
            image = self.preprocess(image).unsqueeze(0).to(self.device)
            with torch.no_grad():
                image_feature = self.model.encode_image(image)

        return image_feature
    