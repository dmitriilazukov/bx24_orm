# -*- coding: utf-8 -*-


class BaseBxAdapter(object):
    def __init__(self, entity_cls):
        self.entity_cls = entity_cls

    def from_bitrix(self, response):
        # type: (BxQueryResponse) -> BxEntity or list
        if response.result:
            if type(response.result) is list:
                return [self.entity_cls(**r) for r in response.result]
            else:
                return self.entity_cls(**response.result)
        else:
            return None

    @classmethod
    def to_bitrix(cls, bx_entity, force_all_fields=False):
        # type: (BxEntity, bool) -> dict
        return bx_entity.get_updates(force_all_fields)
