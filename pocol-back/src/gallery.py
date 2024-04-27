import json
import os
import uuid

from PIL import Image

class Gallery:
    def __init__(self, gallery):
        # self.uuid = uuid
        self.gallery = gallery
        
    
    def get_metadata(self):
        result = {} 
        result.update(self.gallery)
        result["files"] = self.get_gallery_files()
        return result
    
    
    def get_gallery_files(self):
        gallery_path = self.gallery["path"]
        metadata_file = os.path.join(gallery_path, ".metadata")
        metadata = {}
        if not os.path.exists(metadata_file):
            for img in [img for img in os.listdir(gallery_path) if img.lower().endswith(".jpg") or img.lower().endswith(".jpeg") or img.lower().endswith(".png") or img.lower().endswith(".bmp")]:
                im = Image.open(os.path.join(gallery_path, img))
                metadata[uuid.uuid4().hex] = {
                        "path" : os.path.join(gallery_path, img),
                        "width" : im.width,
                        "height" : im.height
                    }
            with open(metadata_file, "w") as f:
                json.dump(metadata, f)
        else:
            with open(metadata_file, "r") as f:
                metadata = json.load(f)
        return metadata
    
    
    def get_image_path(self, uuid):
        files = self.get_gallery_files()
        if uuid in list(files.keys()):
            return files[uuid]["path"]
        else:
            return "not found"
        
        
    def get_image_thumb(self, uuid):
        path = self.get_image_path(uuid)
        thumb_path = path + ".thumb"
        if not os.path.exists(thumb_path):
            im = Image.open(path)
            height = 256
            width = 256 * (im.width / im.height)
            im.thumbnail((width, height), Image.Resampling.LANCZOS)
            im.save(thumb_path, "JPEG")
        return thumb_path
    
    
    def get_firts_thumb_path(self):
        files = self.get_gallery_files()
        if len(list(files.keys())) > 0:
            return self.get_image_thumb(list(files.keys())[0])
        else:
            return "not found"