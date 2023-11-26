from domains.cabinet import Cabinet
from repository.adapters.base_sql_repo import BaseRepo
from repository.model.cabinet import BoardSchema, CabinetSchema
from ..protocols.cabinet_repo_meta import CabinetRepo


class CabinetRepoImpl(BaseRepo[CabinetSchema], CabinetRepo):
    def __init__(self, session_factory):
        super().__init__(
            model=CabinetSchema,
            session_factory=session_factory,
            primary_key_identifier="cabinet_id",
        )

    def get_all_by_topic(self, topic: str):
        with self.session_factory() as session:
            bulks = session.query(self.model).filter(self.model.topic == topic).all()
            return bulks

    def get_all_by_user_id(self, user_id) -> list[Cabinet]:
        with self.session_factory() as session:
            bulks = session.query(self.model).filter(self.model.author == user_id).all()

            def _conv(model):
                ent = self.db_to_entity(model)
                if ent is None:
                    raise Exception("")
                return ent

            return list(map(_conv, bulks))

    def db_to_entity(self, db_data: CabinetSchema | None) -> Cabinet | None:
        def schemaConverter(board_schema: BoardSchema) -> str:
            return board_schema.board_id

        if db_data is not None:
            return Cabinet(
                cabinetId=db_data.cabinet_id,
                name=db_data.name,
                author=db_data.author,
                # boardRefs=list(map(schemaConverter,db_data.board_id_refs)),
                createdOn=float(db_data.created_on.timestamp()),
            )

    def entity_to_db(
        self, cabinet_domain: Cabinet | None, to_dict=False
    ) -> CabinetSchema | dict | None:
        if cabinet_domain is not None:
            cd = cabinet_domain
            _dict_res = {
                "cabinet_id": cd.cabinetId,
                "name": cd.name,
                "author": cd.author,
            }

            if not to_dict:
                return CabinetSchema(**_dict_res)
            else:
                return _dict_res

    def updateBoardRefs(self, boardRef):
        pass

    # def update(self, cabinet_id : str,detail: CabinetPatcher):
    #     print("detail",detail)
    #     return "true"
