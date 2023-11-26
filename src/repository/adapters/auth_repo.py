from domains.auth import (
    TokenCredential,
)
from ..protocols.auth_repo_meta import AuthRepo
from ..model.auth import TokenSchema
from .base_sql_repo import BaseRepo


class AuthRepoImpl(BaseRepo[TokenSchema], AuthRepo):
    model: TokenSchema

    def __init__(self, session_factory):
        super().__init__(model=TokenSchema, session_factory=session_factory)

    def fetch_refresh_token(self, user_id: str):
        with self.session_factory() as session:
            existed = (
                session.query(self.model).filter(self.model.user_id == user_id).first()
            )

            return self.db_to_entity(existed)

    def db_to_entity(
        self, token_schema_data: TokenSchema | None
    ) -> TokenCredential | None:
        tkd = token_schema_data
        if tkd is not None:
            return TokenCredential.create(
                tokenType=tkd.token_type,
                tokenValue=tkd.token_value,
                expireAt=tkd.expire_at,
            )
        pass

    def entity_to_db(
        self, user_id: str, tokenCred: TokenCredential | None
    ) -> TokenSchema | None:
        if tokenCred is not None:
            return self.model(
                jti=tokenCred.jti,
                user_id=user_id,
                token_type=tokenCred.tokenType,
                token_value=tokenCred.tokenValue.get_secret_value(),
                expire_at=int(tokenCred.expireAt),
            )

    def append_refresh_token(self, user_id: str, token: TokenCredential):
        with self.session_factory() as session:
            _data = self.entity_to_db(user_id, token)
            session.add(_data)
            session.commit()
            session.refresh(_data)
