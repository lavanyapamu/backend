from flask_restx import Namespace
 
class ArtworkDTO:
    api = Namespace("artworks", description="artworks")