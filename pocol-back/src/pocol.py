import json
import os
import uuid

from gallery import Gallery

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
                self.gallery_objects[new_gallery_uuid]["file_count"] = len(Gallery(self.gallery_objects[new_gallery_uuid]).get_metadata()["files"])
        
    
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
            return Gallery(self.gallery_objects[uuid])
        else:
            print(f"gallery {uuid} not found")
            return "not found"
