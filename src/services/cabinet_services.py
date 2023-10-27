from repository.protocols.cabinet_repo_meta  import CabinetRepo
from domains.cabinet import Cabinet
from schemas.cabinet import CreateCabinet

class CabinetService:
    repo : CabinetRepo

    def __init__(self, repo: CabinetRepo):
        self.repo = repo

    def getAllCabinets(self, user_id: str):
        items = self.repo.get_all_by_user_id(user_id)
        return items

    def createCabinet(self, cabinet_data: CreateCabinet):
        newCabinet = Cabinet.create(name=cabinet_data.cabinetName,author=cabinet_data.authorId)
        dto = self.repo.entity_to_db(newCabinet)
        dbResult = self.repo.add(dto);

        return dbResult

