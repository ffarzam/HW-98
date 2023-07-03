import os
import shutil
from unittest import TestCase, main
from data_manager.file_manager import FileManager, BaseModel


class TestModel(BaseModel):
    data: str

    def __init__(self, data="Test") -> None:
        super().__init__()
        self.data = data

    def __str__(self) -> str:
        return f'TestModel #{self._id}: {self.data}'


class FileManagerTest(TestCase):
    config = {
        'ROOT_PATH': 'test_data/'
    }
    manager = FileManager(config)

    def setUp(self) -> None:
        root_files_path = self.config['ROOT_PATH']
        if os.path.exists(root_files_path):
            shutil.rmtree(root_files_path)

    def tearDown(self) -> None:
        root_files_path = self.config['ROOT_PATH']
        if os.path.exists(root_files_path):
            shutil.rmtree(root_files_path)

    def test1_create(self):
        test_model = TestModel("Test1")

        # Check if id is not set
        self.assertIsNone(getattr(test_model, '_id', None))

        # Creating
        self.manager.create(test_model)

        # Check if id is set
        self.assertIsNotNone(getattr(test_model, '_id', None))

    def test2_create_read(self):
        test_model = TestModel("Test2")

        # Creating
        self.manager.create(test_model)

        read_model = self.manager.read(test_model._id, test_model.__class__)
        self.assertIsNotNone(read_model)

        self.assertRaises(FileNotFoundError, self.manager.read, 100, test_model.__class__)

    def test3_read_all(self):
        num_of_objs = 5
        models = []
        for i in range(num_of_objs):
            m = TestModel("Test" + str(i))
            self.manager.create(m)
            models.append(m)

        all_models = list(self.manager.read_all(TestModel))

        for m in models:
            self.assertIn(m, all_models)

    def test4_update(self):

        test_model = TestModel("Test")
        self.manager.create(test_model)
        test_model.data = "Test2"

        self.manager.update(test_model)
        m = self.manager.read(test_model._id, test_model.__class__)
        self.assertEqual(m.data, "Test2")

    def test5_shift_delete(self):
        test_model = TestModel("Test")
        self.manager.create(test_model)
        m = self.manager.read(test_model._id, test_model.__class__)
        self.manager.shift_delete(test_model._id, test_model.__class__)
        all_models = list(self.manager.read_all(TestModel))
        self.assertNotIn(m, all_models)
        self.assertRaises(FileNotFoundError, self.manager.shift_delete, 100, test_model.__class__)

    def test6_delete(self):
        test_model = TestModel("Test")
        self.manager.create(test_model)
        m = self.manager.read(test_model._id, test_model.__class__)
        self.manager.delete(test_model._id, test_model.__class__)
        all_models = list(self.manager.read_all(TestModel))
        self.assertNotIn(m, all_models)
        self.assertRaises(FileNotFoundError, self.manager.delete, 100, test_model.__class__)
        shutil.rmtree(os.path.join(os.getcwd(), "Recycle Bin"))

    def test7_retrieve(self):
        test_model = TestModel("Test")
        self.manager.create(test_model)
        m = self.manager.read(test_model._id, test_model.__class__)
        self.manager.delete(test_model._id, test_model.__class__)
        self.manager.retrieve(test_model._id, test_model.__class__)
        m = self.manager.read(test_model._id, test_model.__class__)
        all_models = list(self.manager.read_all(TestModel))
        self.assertIn(m, all_models)
        self.assertRaises(FileNotFoundError, self.manager.retrieve, 100, test_model.__class__)
        shutil.rmtree(os.path.join(os.getcwd(), "Recycle Bin"))

    def test8_truncate(self):

        m = TestModel("Test")
        self.manager.create(m)

        files = os.listdir(self.manager.files_root + '/')
        self.assertEqual(len(files), 1)

        self.manager.truncate(m.__class__)
        files = os.listdir(self.manager.files_root + '/')
        self.assertEqual(len(files), 0)


if __name__ == '__main__':
    main()
