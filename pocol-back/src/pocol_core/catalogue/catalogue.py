import json
import os
import unittest
import logging
import sys


CATALOGUE_FILE_NAME = "catalogue.json"

CATEGORIES = "categories"
PARENTS = "parents"
OBJECTS = "objects"

class CategoryAlreadyExists(Exception): pass
class CategoryNotExists(Exception): pass
class ParentCategoryNotExists(Exception): pass


class Catalogue:
    def __init__(self, fileName):
        self.fileName = fileName
        self.data = {CATEGORIES: {}}
        self.load()
    
    def dump(self):
        if self.fileName != ":MEMORY:":
            with open(self.fileName, 'w') as f:
                json.dump(self.data, f, sort_keys=True, indent=2)
    
    def load(self):
        if self.fileName != ":MEMORY:":
            if not os.path.exists(self.fileName):
                self.dump()
            self.__load__()

    def __load__(self):
        if self.fileName != ":MEMORY:":
            with open(self.fileName, 'r') as f:
                self.data = json.load(f)
    
    def addCategory(self, name):
        if name in self.data[CATEGORIES]:
            raise CategoryAlreadyExists()
        self.data[CATEGORIES][name] = {PARENTS: [], OBJECTS: []}
        self.dump()
    
    def getCategory(self, name):
        print(name)
        if name in self.data[CATEGORIES]:
            return CatalogueCategory(self, name)
        else:
            raise CategoryNotExists()
    
    def removeCategory(self, name):
        if name in self.data[CATEGORIES]:
            del self.data[CATEGORIES][name]
            for c in self.data[CATEGORIES]:
                if name in c[PARENTS]:
                    del c[PARENTS][name]
            self.dump()
        else:
            raise CategoryNotExists()

    def getCategories(self):
        return [CatalogueCategory(self, c) for c in self.data[CATEGORIES].keys()]


class CatalogueCategory:
    def __init__(self, catalogue, name):
        self.catalogue = catalogue
        self.name = name
        
    def getName(self):
        return self.name
    
    def getAllParents(self):
        parent_names = list(self.catalogue.data[CATEGORIES][self.name][PARENTS])
        for parent_name in parent_names:
            next_parents_names = [c.getName() for c in self.catalogue.getCategory(parent_name).getAllParents()]
            parent_names.extend([n for n in next_parents_names if n not in parent_names])
        return [CatalogueCategory(self.catalogue, c) for c in parent_names]
    
    def addParent(self, parent_name):
        parent_names = self.getAllParents()
        if parent_name in parent_names:
            return
        self.catalogue.data[CATEGORIES][self.name][PARENTS].append(parent_name)
        self.catalogue.dump()

    def getSubcategories(self, max_lvl=1):
        result = []
        if max_lvl > 0:
            categories = self.catalogue.data[CATEGORIES]
            result = [self.catalogue.getCategory(cn) for cn in categories.keys() if self.name in categories[cn][PARENTS]]
            for c in result:
                subs = self.catalogue.getCategory(c.getName()).getSubcategories(max_lvl - 1)
                result.extend([s for s in subs if s.getName() not in [s.getName() for s in result]])
        return result
    
    def assign(self, object_uuid):
        self.getAllParents()
        
        
class CatalogueTests(unittest.TestCase):
    def testAddCategory1(self):
        catalogue = Catalogue(":MEMORY:")
        self.assertEqual(len(catalogue.getCategories()), 0)
        catalogue.addCategory("test1")
        self.assertEqual(len(catalogue.getCategories()), 1)
        self.assertEqual(catalogue.getCategories()[0].getName(), "test1")
    
    def testAddCategory2(self):
        catalogue = Catalogue(":MEMORY:")
        self.assertEqual(len(catalogue.getCategories()), 0)
        catalogue.addCategory("test1")
        catalogue.addCategory("test2")
        self.assertEqual(len(catalogue.getCategories()), 2)
        self.assertTrue(catalogue.getCategories()[0].getName() in ["test1", "test2"])
        self.assertTrue(catalogue.getCategories()[1].getName() in ["test1", "test2"])

    def testGetCategory(self):
        catalogue = Catalogue(":MEMORY:")
        with self.assertRaises(CategoryNotExists):
            catalogue.getCategory("test1")
        catalogue.addCategory("test1")
        self.assertEqual(catalogue.getCategory("test1").getName(), "test1")

    def testAddParent(self):
        catalogue = Catalogue(":MEMORY:")
        catalogue.addCategory("test1")
        catalogue.addCategory("test2.1")
        catalogue.addCategory("test2.2")
        catalogue.addCategory("test3")
        catalogue.getCategory("test3").addParent("test2.1")
        catalogue.getCategory("test3").addParent("test2.2")
        catalogue.getCategory("test2.1").addParent("test1")
        self.assertTrue("test1" in catalogue.getCategory("test3").getAllParents())
        self.assertTrue("test2.1" in catalogue.getCategory("test3").getAllParents())
        self.assertTrue("test2.2" in catalogue.getCategory("test3").getAllParents())
        self.assertTrue("test1" in catalogue.getCategory("test2.1").getAllParents())
        
    def testGetSubcategories(self):
        catalogue = Catalogue(":MEMORY:")
        catalogue.addCategory("test1")
        catalogue.addCategory("test2.1")
        catalogue.addCategory("test2.2")
        catalogue.addCategory("test3")
        catalogue.getCategory("test3").addParent("test2.1")
        catalogue.getCategory("test3").addParent("test2.2")
        catalogue.getCategory("test2.1").addParent("test1")
        self.assertEqual(len(catalogue.getCategory("test1").getSubcategories()), 1)
        self.assertTrue("test2.1" in [c.getName() for c in catalogue.getCategory("test1").getSubcategories()])
        self.assertEqual(len(catalogue.getCategory("test1").getSubcategories(max_lvl=2)), 2)
        self.assertTrue("test2.1" in [c.getName() for c in catalogue.getCategory("test1").getSubcategories(max_lvl=2)])
        self.assertTrue("test3" in [c.getName() for c in catalogue.getCategory("test1").getSubcategories(max_lvl=2)])
        

    
if __name__ == '__main__':
    logging.basicConfig( stream=sys.stderr )
    unittest.main()