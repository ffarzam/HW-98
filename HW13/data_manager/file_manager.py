import os
from typing import Generator, Any
from data_manager.base import BaseModel, BaseManager
import pickle


class FileManager(BaseManager):
    ROOT_PATH_CONFIG_KEY = 'ROOT_PATH'

    def __init__(self, config: dict) -> None:
        """
        Initializes a new instance of the FileManager class.

        Args:
            config (dict): The configuration dictionary for the FileManager instance.
        """
        super().__init__(config)

    @property
    def files_root(self):
        """
        Returns the root directory for the file manager.

        Returns:
            str: The root directory.
        """
        root_dir = self.config[self.ROOT_PATH_CONFIG_KEY]
        if not os.path.exists(root_dir):
            os.mkdir(root_dir)
        return root_dir

    def _get_id(self, model_type: type) -> int:
        """
        Gets the maximum ID for the specified model type.

        Args:
            model_type (type): The model type to get the ID for.

        Returns:
            int: The maximum ID for the specified model type.
        """
        files = os.listdir(self.files_root + '/')
        ids = []
        for f in files:
            if f.startswith(model_type.__name__):
                ids.append(int(f.split('_')[-1].split('.')[0]))
        return max(ids) + 1 if ids else 1

    def _get_file_path(self, _id, model_type: type) -> str:
        """
        Gets the file path for the model instance with the specified ID and type.

        Args:
            _id (int): The ID of the model instance.
            model_type (type): The type of the model instance.

        Returns:
            str: The file path for the model instance.
        """
        # return f"{self.files_root}/{model_type.__name__}_{_id}.pkl".replace('//', '/')
        return os.path.join(self.files_root, f"{model_type.__name__}_{_id}.pkl")

    def create(self, m: BaseModel) -> Any:
        """
        Creates a new model instance.

        Args:
            m (BaseModel): The model instance to create.

        Returns:
            Any: The path to the created file.
        """
        m._id = self._get_id(m.__class__)  # set ID!!!!
        file_path = self._get_file_path(m._id, m.__class__)
        with open(file_path, "wb") as f:
            pickle.dump(m, f)
        return file_path

    def read(self, id: int, model_cls: type) -> BaseModel:
        """
        Reads a model instance from the file system.

        Args:
            id (int): The ID of the model instance to read.
            model_cls (type): The type of the model instance.

        Returns:
            BaseModel: The model instance.
        """
        file_path = self._get_file_path(id, model_cls)
        try:
            with open(file_path, "rb") as f:
                m = pickle.load(f)
                return m
        except FileNotFoundError:
            raise FileNotFoundError(f"File with ID {id} does not exist.")

    def update(self, m: BaseModel) -> None:
        """
        Updates an existing model instance.

        Args:
            m (BaseModel): The model instance to update.
        """
        with open(self._get_file_path(m._id, m.__class__), "wb") as f:
            pickle.dump(m, f)

    def delete(self, id: int, model_cls: type) -> None:
        """
        Deletes a model instance from the file system temporarily.

        Args:
            id (int): The ID of the model instance to delete.
            model_cls (type): The type of the model instance.
        """
        if not os.path.exists(os.path.join(os.getcwd(), "Recycle Bin")):
            os.mkdir(os.path.join(os.getcwd(), "Recycle Bin"))

        try:
            os.rename(self._get_file_path(id, model_cls),
                      os.path.join(os.getcwd(), "Recycle Bin", f"{model_cls.__name__}_{id}.pkl"))
        except FileNotFoundError:
            raise FileNotFoundError(f"File with ID {id} does not exist.")

    def shift_delete(self, id: int, model_cls: type) -> None:
        """
        Deletes a model instance from the file system permanently.

        Args:
            id (int): The ID of the model instance to delete.
            model_cls (type): The type of the model instance.
        """
        try:
            os.remove(self._get_file_path(id, model_cls))

        except FileNotFoundError:
            raise FileNotFoundError(f"File with ID {id} does not exist.")

    def read_all(self, model_cls: type | None = None) -> Generator:
        """
        Reads all model instances from the file system.

        Args:
            model_cls (type): The type of the model instances to read.

        Yields:
            BaseModel: The next model instance.
        """
        files = os.listdir(self.files_root + '/')

        for item in files:

            file_path = os.path.join(self.files_root, item)

            if not model_cls:
                with open(file_path, "rb") as f:
                    m = pickle.load(f)

            elif item.split('_')[0] == model_cls.__name__:
                with open(file_path, "rb") as f:
                    m = pickle.load(f)
            yield m

    def truncate(self, model_cls: type) -> None:
        """
        Deletes all model instances of the specified type from the file system.

        Args:
            model_cls (type): The type of the model instances to delete.
        """
        files = os.listdir(self.files_root + '/')
        for item in files:
            file_path = os.path.join(self.files_root, item)
            if model_cls is None:
                os.remove(file_path)

            elif item.split('_')[0] == model_cls.__name__:
                os.remove(file_path)

    def retrieve(self, id: int, model_cls: type) -> None:
        try:
            os.replace(os.path.join(os.getcwd(), "Recycle Bin", f"{model_cls.__name__}_{id}.pkl"),
                       self._get_file_path(id, model_cls))
        except FileNotFoundError:
            raise FileNotFoundError(f"File with ID {id} does not exist.")
