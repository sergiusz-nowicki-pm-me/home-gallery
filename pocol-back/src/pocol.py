import json
import os
import uuid

from PIL import Image

class Pocol:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        
        self.gallery_list_file = os.path.join(base_dir, ".gallery_list.metadata")
        self.gallery_list = {}

        self.gallery_objects_file = os.path.join(base_dir, ".galleries.metadata")
        self.gallery_objects = {}   

    
    def init(self):
        galleries = self.load_galleries()
        self.load_gallery_list_metadata()
        self.load_gallery_objects_metadata()
        self.add_new_galleries(galleries)
        self.remove_missing_galleries(galleries)
        self.dump_metadata()
        print("init finished")
        
        
    def load_galleries(self):
        print("loading galleries")
        galleries = []
        for root, dirs, files in os.walk(self.base_dir):
            if len(files) > 0 and root != self.base_dir:
                galleries.append(root)
        print(f"found {len(galleries)} galleries")
        return galleries
        
    
    def load_gallery_list_metadata(self):
        if not os.path.exists(self.gallery_list_file):
            print("creating gallery list file")
            with open(self.gallery_list_file, "w") as f:
                json.dump(self.gallery_list, f, indent=4)
        else:
            print("loading gallery list files")
            with open(self.gallery_list_file, "r") as f:
                self.gallery_list = json.load(f)
        
        
    def load_gallery_objects_metadata(self):
        if not os.path.exists(self.gallery_objects_file):
            print("creating gallery objects file")
            with open(self.gallery_objects_file, "w") as f:
                json.dump(self.gallery_objects, f, indent=4)
        else:
            print("loading gallery objects file")
            with open(self.gallery_objects_file, "r") as f:
                self.gallery_objects = json.load(f)
        
        
    def add_new_galleries(self, galleries):
        print("adding new galleries")
        index = 1
        for g in galleries:
            print(f"processing gallery {index}", end="\r")
            index += 1
            if g not in self.gallery_list.keys():
                new_gallery_uuid = uuid.uuid4().hex
                self.gallery_list[g] = new_gallery_uuid
                self.gallery_objects[new_gallery_uuid] = {
                    "path": g
                }         
                self.gallery_objects[new_gallery_uuid]["file_count"] = len(Gallery(new_gallery_uuid, self.gallery_objects[new_gallery_uuid]).get_metadata()["files"])
        
    
    def remove_missing_galleries(self, galleries):
        for m in list(self.gallery_list.keys()):
            if not m in galleries:
                # delete gallery object
                del self.gallery_objects[self.gallery_list[m]]
                # delete gallery id
                del self.gallery_list[m]
        
        
    def dump_metadata(self):
        print("dumping metadata")

        with open(self.gallery_list_file, "w") as f:
            json.dump(self.gallery_list, f, indent=4)

        with open(self.gallery_objects_file, "w") as f:
            json.dump(self.gallery_objects, f, indent=4)
        
    
    def list_all_galleries(self):
        return self.gallery_objects
    
    
    def get_gallery(self, uuid):
        if uuid in self.gallery_objects:
            return Gallery(uuid, self.gallery_objects[uuid])
        else:
            print(f"gallery {uuid} not found")
            return "not found"
    
    
class Gallery:
    def __init__(self, uuid, gallery):
        self.uuid = uuid
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