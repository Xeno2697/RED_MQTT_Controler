# coding: utf-8
#送信されてきた画像データの情報を管理するクラス
from typing import Dict



class ImageInformation:
    def __init__(self) -> None:
        self.__ImageName = ""
        self.__ImageData = b''
        
    def decode_json_data(self, data: Dict) -> None:
        self.__ImageName = str(data.keys()[0])
        self.__ImageData = data[self.__ImageName]